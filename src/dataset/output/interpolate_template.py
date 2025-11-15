import re
import json
from typing import Any, Dict, List, Optional, Callable

# --- Auxiliary Functions ---
# These functions are defined at the module level for clarity,
# but are intended for internal use by interpolate_template.

# Regex patterns for parsing template expressions and literals
_VAR_PATH_RE = re.compile(r'([a-zA-Z_][a-zA-Z0-9_.]*(?:\[\d+\])?)')
_COMPARISON_RE = re.compile(r'^\s*(' + _VAR_PATH_RE.pattern + r')\s*(==|!=)\s*(.*)\s*$')
_NOT_RE = re.compile(r'^\s*not\s+(' + _VAR_PATH_RE.pattern + r')\s*$')

_LITERAL_INT_RE = re.compile(r'^\s*[-+]?\d+\s*$')
_LITERAL_FLOAT_RE = re.compile(r'^\s*[-+]?\d*\.\d+(?:[eE][-+]?\d+)?\s*$')
_LITERAL_BOOL_RE = re.compile(r'^\s*(true|false)\s*$', re.IGNORECASE)
_LITERAL_NONE_RE = re.compile(r'^\s*none\s*$', re.IGNORECASE)
_LITERAL_STRING_QUOTED_RE = re.compile(r"""^\s*(['"])(.*?)\1\s*$""") # Captures content inside quotes

def _parse_literal(literal_str: str) -> Any:
    """Safely parses a string into its literal Python type (int, float, bool, None, or string)."""
    s = literal_str.strip()
    if _LITERAL_INT_RE.match(s):
        return int(s)
    if _LITERAL_FLOAT_RE.match(s):
        return float(s)
    if _LITERAL_BOOL_RE.match(s):
        return s.lower() == 'true'
    if _LITERAL_NONE_RE.match(s):
        return None
    match = _LITERAL_STRING_QUOTED_RE.match(s)
    if match:
        return match.group(2) # Return content inside quotes
    return s # Default to string if no other literal type matches

def _resolve_path_with_index(context: Dict[str, Any], path_str: str) -> Any:
    """
    Resolves a dot-separated path (e.g., 'user.profile.name') or
    indexed path (e.g., 'items[0].value') within a context dictionary.
    Returns None if any part of the path is not found or invalid.
    """
    parts = re.findall(r'(\w+)(?:\[(\d+)\])?', path_str) # [(attr_or_key, index_str or None), ...]
    current = context
    for part, index_str in parts:
        if isinstance(current, dict):
            if part in current:
                current = current[part]
            else:
                return None
        elif hasattr(current, part):
            current = getattr(current, part)
        else:
            return None
        
        if index_str: # If an index was specified (e.g., 'items[0]')
            try:
                index = int(index_str)
                if isinstance(current, (list, tuple)) and 0 <= index < len(current):
                    current = current[index]
                else:
                    return None # Not a list/tuple or index out of bounds
            except ValueError:
                return None # Should not happen with regex, but for safety
    return current

def _evaluate_expression(expression: str, context: Dict[str, Any]) -> bool:
    """
    Safely evaluates a simple boolean expression.
    Supported forms:
    - 'variable.path' (truthiness)
    - 'not variable.path'
    - 'variable.path == literal'
    - 'variable.path != literal'
    """
    expression = expression.strip()

    # Try "not var.path"
    match = _NOT_RE.match(expression)
    if match:
        var_path_str = match.group(1)
        value = _resolve_path_with_index(context, var_path_str)
        return not bool(value)

    # Try "var.path == literal" or "var.path != literal"
    match = _COMPARISON_RE.match(expression)
    if match:
        var_path_str = match.group(1)
        operator = match.group(2)
        literal_str = match.group(3).strip()

        var_value = _resolve_path_with_index(context, var_path_str)
        literal_value = _parse_literal(literal_str)

        if operator == '==':
            return var_value == literal_value
        elif operator == '!=':
            return var_value != literal_value

    # Try simple variable truthiness "var.path"
    match = _VAR_PATH_RE.match(expression)
    if match:
        var_path_str = match.group(1)
        value = _resolve_path_with_index(context, var_path_str)
        return bool(value)

    raise ValueError(f"Unsupported or malformed expression syntax in conditional block: '{expression}'")

# --- Built-in Filters ---

def _filter_upper(value: Any) -> str:
    """Converts the value to uppercase."""
    return str(value).upper()

def _filter_lower(value: Any) -> str:
    """Converts the value to lowercase."""
    return str(value).lower()

def _filter_default(value: Any, default_value: Any) -> Any:
    """Returns the value if it's not None and not an empty string, otherwise returns the default_value."""
    return value if value is not None and value != '' else default_value

def _filter_trim(value: Any) -> str:
    """Removes leading/trailing whitespace from the value."""
    return str(value).strip()

_FILTERS: Dict[str, Callable[..., Any]] = {
    'upper': _filter_upper,
    'lower': _filter_lower,
    'default': _filter_default,
    'trim': _filter_trim,
}

# --- Main Interpolation Function ---

def interpolate_template(template_string: str, context: Dict[str, Any]) -> str:
    """
    Renders templates with nested variable substitution, filters, and conditional blocks.

    Args:
        template_string: The template content as a string.
        context: A dictionary containing variables to be substituted.

    Returns:
        The rendered template string.

    Raises:
        ValueError: If there's a syntax error in a template tag or an unknown command.
    """
    output_buffer: List[str] = []

    # Regex to find all template tags (variable or block)
    # Group 1 captures content for {{...}}, Group 2 for {%...%}
    _TAG_RE = re.compile(r'\{\{(.*?)\}\}|\{\%(.*?)\%\}', re.DOTALL)

    class BlockState:
        """
        Represents the state of an 'if' block on the stack.
        - active_condition_met: True if any 'if' or 'elif' condition within this block group has evaluated to True.
        - current_branch_is_active: True if the *current* branch (if, elif, or else) should be rendered.
        """
        def __init__(self):
            self.active_condition_met: bool = False
            self.current_branch_is_active: bool = False

    block_stack: List[BlockState] = []
    
    def _is_all_parent_blocks_rendering(current_stack: List[BlockState]) -> bool:
        """Checks if all blocks higher up in the stack (parents) are currently in an active rendering branch."""
        return all(state.current_branch_is_active for state in current_stack)

    last_idx = 0
    for match in _TAG_RE.finditer(template_string):
        # 1. Add plain text before this tag
        text_before_tag = template_string[last_idx:match.start()]
        if text_before_tag:
            # Only append text if all active parent blocks allow rendering
            if _is_all_parent_blocks_rendering(block_stack):
                output_buffer.append(text_before_tag)

        # 2. Process the tag itself
        tag_content_var = match.group(1) # Content of {{...}}
        tag_content_block = match.group(2) # Content of {%...%}

        if tag_content_var is not None:
            # This is a variable substitution tag {{ ... }}
            if _is_all_parent_blocks_rendering(block_stack):
                try:
                    # Split into variable path and filters (e.g., 'user.name | upper | default("N/A")')
                    parts = [p.strip() for p in tag_content_var.split('|')]
                    var_expr = parts[0]
                    filters_exprs = parts[1:]

                    # Resolve variable value
                    value = _resolve_path_with_index(context, var_expr)
                    
                    # Apply filters sequentially
                    for f_expr in filters_exprs:
                        # Parse filter name and arguments (e.g., 'default("N/A")')
                        f_name_match = re.match(r'([a-zA-Z_][a-zA-Z0-9_]*)(?:\((.*)\))?', f_expr)
                        if not f_name_match:
                            raise ValueError(f"Malformed filter expression: {f_expr}")
                        
                        filter_name = f_name_match.group(1)
                        filter_args_str = f_name_match.group(2) # e.g., '"N/A"' or '123, True'

                        filter_func = _FILTERS.get(filter_name)
                        if not filter_func:
                            raise ValueError(f"Unknown filter: '{filter_name}'")
                        
                        args = []
                        if filter_args_str:
                            # Use json.loads to safely parse complex arguments
                            # Example: "arg1", 'arg2', 123, True, None
                            # This handles quoted strings, numbers, booleans, null
                            # Using regex to split by comma, respecting quoted strings
                            arg_tokens = re.findall(r"(?:'(?:[^'\\]|\\.)*'|\"(?:[^\"\\]|\\.)*\"|[^,])+", filter_args_str)
                            args = [_parse_literal(arg_token.strip()) for arg_token in arg_tokens]

                        value = filter_func(value, *args)

                    output_buffer.append(str(value if value is not None else ''))
                except Exception as e:
                    # For production, might log error and append empty string or default value.
                    # For this implementation, we append an empty string for robustness.
                    output_buffer.append('')
                    # raise # Uncomment to re-raise for strict error handling during development
        else:
            # This is a block tag {% ... %}
            tag_command = tag_content_block.strip()
            
            if tag_command.startswith('if '):
                condition_expr = tag_command[3:].strip()
                condition_result = _evaluate_expression(condition_expr, context)
                
                new_block_state = BlockState()
                new_block_state.active_condition_met = condition_result
                # This branch is active if its condition is true AND all parent blocks are active
                new_block_state.current_branch_is_active = condition_result and _is_all_parent_blocks_rendering(block_stack)
                block_stack.append(new_block_state)

            elif tag_command.startswith('elif '):
                if not block_stack:
                    raise ValueError("Found 'elif' without a preceding 'if' block.")
                
                current_block_state = block_stack[-1]
                
                # An 'elif' branch is only considered if no prior condition in this block group was met
                # AND all parent blocks are active.
                if current_block_state.active_condition_met or not _is_all_parent_blocks_rendering(block_stack[:-1]):
                    current_block_state.current_branch_is_active = False # Skip this elif
                else:
                    condition_expr = tag_command[5:].strip()
                    condition_result = _evaluate_expression(condition_expr, context)
                    current_block_state.active_condition_met = condition_result # Mark if this elif condition is met
                    current_block_state.current_branch_is_active = condition_result # This branch is active if its condition is true

            elif tag_command == 'else':
                if not block_stack:
                    raise ValueError("Found 'else' without a preceding 'if' block.")
                
                current_block_state = block_stack[-1]

                # An 'else' branch is only considered if no prior condition in this block group was met
                # AND all parent blocks are active.
                if current_block_state.active_condition_met or not _is_all_parent_blocks_rendering(block_stack[:-1]):
                    current_block_state.current_branch_is_active = False # Skip this else
                else:
                    current_block_state.current_branch_is_active = True # This branch is active

            elif tag_command == 'endif':
                if not block_stack:
                    raise ValueError("Found 'endif' without a preceding 'if' block.")
                block_stack.pop()

            else:
                raise ValueError(f"Unknown block command: '{tag_command}'")
        
        last_idx = match.end()

    # 3. Add any remaining plain text after the last tag
    remaining_text = template_string[last_idx:]
    if remaining_text:
        if _is_all_parent_blocks_rendering(block_stack):
            output_buffer.append(remaining_text)

    # If there are unclosed blocks, raise an error
    if block_stack:
        raise ValueError("Unclosed conditional blocks found at the end of the template.")

    return "".join(output_buffer)

# add this ad the end of the file
EXPORT_FUNCTION = interpolate_template