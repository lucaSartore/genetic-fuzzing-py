from typing import TypedDict


class FunctionType(TypedDict):
    name: str
    description: str

FUNCTIONS: list[FunctionType] = [
    {
        "name": "roman_to_int",
        "description": "Converts a Roman numeral string (e.g., 'MCMXCIV') to an integer. (Complex validation rules).",
    },
    {
        "name": "int_to_roman",
        "description": "Converts an integer (1-3999) to its Roman numeral representation. (Complex branching).",
    },
    {
        "name": "is_valid_parentheses",
        "description": "Checks if a string of '()[]{}' is balanced and properly nested. (Uses a stack).",
    },
    {
        "name": "longest_substring_without_repeating",
        "description": "Finds the length of the longest substring without repeating characters. (Sliding window).",
    },
    {
        "name": "longest_palindromic_substring",
        "description": "Finds the longest substring that is a palindrome. (Dynamic Programming or expand-around-center).",
    },
    {
        "name": "string_to_integer_atoi",
        "description": "Implements the 'atoi' function, parsing a string to an integer with edge cases (whitespace, sign, overflow).",
    },
    {
        "name": "compare_version_numbers",
        "description": "Compares two version strings (e.g., '1.0.1' vs '1.1').",
    },
    {
        "name": "simplify_path",
        "description": "Simplifies a Unix-style absolute path (e.g., '/a/./b/../../c/' -> '/c').",
    },
    {
        "name": "text_justification",
        "description": "Takes a list of words and a width, and returns a list of fully justified text lines.",
    },
    {
        "name": "basic_calculator_ii",
        "description": "Evaluates a string expression with '+', '-', '*', '/' and no parentheses. (Shunting-yard or stack-based).",
    },
    {
        "name": "decode_string",
        "description": "Decodes a string like '3[a]2[bc]' into 'aaabcbc'. (Recursive or stack-based).",
    },
    {
        "name": "is_valid_ip_address",
        "description": "Checks if a string is a valid IPv4 or IPv6 address. (Lots of string splitting and validation).",
    },
    {
        "name": "parse_simple_ini",
        "description": "Parses a simple .ini format string into a dictionary of dictionaries.",
    },
    {
        "name": "levenshtein_distance",
        "description": "Calculates the edit distance between two strings. (Dynamic Programming).",
    },
    {
        "name": "word_search",
        "description": "Finds a word in a 2D grid of characters. (Backtracking).",
    },
    {
        "name": "count_and_say",
        "description": "Generates the n-th term of the 'count-and-say' sequence.",
    },
    {
        "name": "group_anagrams",
        "description": "Groups a list of strings into lists of anagrams.",
    },
    {
        "name": "find_all_anagrams",
        "description": "Finds all starting indices of 'p's anagrams in 's'. (Sliding window with character counts).",
    },
    {
        "name": "reverse_words",
        "description": "Reverses the order of words in a string, handling whitespace.",
    },
    {
        "name": "zigzag_conversion",
        "description": "Converts a string into a zigzag pattern and reads it line by line.",
    },
    {
        "name": "merge_k_sorted_lists",
        "description": "Merges 'k' sorted lists into one sorted list. (Can be simulated with lists, good for 'heapq').",
    },
    {
        "name": "deserialize_binary_tree",
        "description": "Deserializes a string back into a (simulated) binary tree.",
    },
    {
        "name": "max_sliding_window",
        "description": "Finds the maximum of each sliding window of size 'k'. (Uses 'collections.deque').",
    },
    {
        "name": "trie_insert_and_search",
        "description": "Builds a Trie (as a nested dict) from 'words' and checks if 'prefixes' exist.",
    },
    {
        "name": "find_duplicate_files",
        "description": "Parses a list of strings like 'root/a 1.txt(content)' and finds groups of duplicate file content.",
    },
    {
        "name": "implement_a_queue_using_stacks",
        "description": "Simulates a queue using only two stacks (lists).",
    },
    {
        "name": "implement_a_stack_using_queues",
        "description": "Simulates a stack using only two queues (e.g., 'collections.deque').",
    },
    {
        "name": "merge_intervals",
        "description": "Merges a list of overlapping intervals '[[1,3],[2,6],[8,10]]'.",
    },
    {
        "name": "task_scheduler",
        "description": "Schedules a list of tasks (e.g., ['A','A','B']) with a cooldown 'n'.",
    },
    {
        "name": "find_itinerary",
        "description": "Reconstructs a flight itinerary from a list of '[from, to]' tickets. (Graph traversal).",
    },
    {
        "name": "word_ladder",
        "description": "Finds the shortest transformation sequence from 'begin_word' to 'end_word'. (BFS).",
    },
    {
        "name": "three_sum",
        "description": "Finds all unique triplets in a list that sum to zero.",
    },
    {
        "name": "container_with_most_water",
        "description": "Finds the two lines that, with the x-axis, form a container holding the most water.",
    },
    {
        "name": "letter_combinations_of_phone_number",
        "description": "Generates all possible letter combinations from a digit string. (Backtracking).",
    },
    {
        "name": "generate_parentheses",
        "description": "Generates all valid combinations of 'n' pairs of parentheses. (Backtracking).",
    },
    {
        "name": "next_permutation",
        "description": "Finds the next lexicographically greater permutation of a list of numbers.",
    },
    {
        "name": "search_in_rotated_sorted_array",
        "description": "Searches for a target in a sorted array that has been rotated. (Modified binary search).",
    },
    {
        "name": "combination_sum",
        "description": "Finds all unique combinations from 'candidates' that sum to 'target'. (Backtracking).",
    },
    {
        "name": "spiral_matrix",
        "description": "Returns all elements of a matrix in spiral order.",
    },
    {
        "name": "jump_game",
        "description": "Determines if you can reach the last index of an array given jump lengths. (Greedy or DP).",
    },
    {
        "name": "unique_paths",
        "description": "Finds the number of unique paths from (0,0) to (m,n) in a grid, moving only right or down. (DP).",
    },
    {
        "name": "climbing_stairs",
        "description": "Finds the number of distinct ways to climb 'n' stairs, taking 1 or 2 steps at a time. (Simple DP).",
    },
    {
        "name": "longest_common_subsequence",
        "description": "Finds the length of the longest common subsequence. (DP).",
    },
    {
        "name": "word_break",
        "description": "Checks if 's' can be segmented into a space-separated sequence of words from 'word_dict'. (DP).",
    },
    {
        "name": "coin_change",
        "description": "Finds the fewest number of coins needed to make 'amount'. (DP).",
    },
    {
        "name": "longest_increasing_subsequence",
        "description": "Finds the length of the LIS. (DP).",
    },
    {
        "name": "course_schedule",
        "description": "Checks if all courses can be finished, given '[course, prereq]' pairs. (Topological sort).",
    },
    {
        "name": "house_robber",
        "description": "Finds the maximum amount you can rob from houses in a line without robbing adjacent ones. (DP).",
    },
    {
        "name": "largest_rectangle_in_histogram",
        "description": "Finds the largest rectangle area in a histogram.",
    },
    {
        "name": "median_of_two_sorted_arrays",
        "description": "Finds the median of two sorted arrays.",
    },
    {
        "name": "n_queens_solver",
        "description": "Finds all distinct solutions to the N-Queens puzzle. (Backtracking).",
    },
    {"name": "sudoku_solver", "description": "Solves a Sudoku puzzle. (Backtracking)."},
    {
        "name": "is_prime",
        "description": "Checks if an integer 'n' is a prime number. (Edge cases: 0, 1, negatives, large numbers).",
    },
    {
        "name": "extended_gcd",
        "description": "Implements the extended Euclidean algorithm.",
    },
    {
        "name": "pow_int",
        "description": "Implements 'pow(x, n)' for integers, handling negative exponents.",
    },
    {
        "name": "sqrt_int",
        "description": "Finds the integer square root of 'x' using binary search.",
    },
    {
        "name": "is_number",
        "description": "Validates if a string represents a valid number (e.g., '-1.2e+5'). (Extremely complex edge cases).",
    },
    {
        "name": "fraction_to_recurring_decimal",
        "description": "Converts a fraction to a string, handling recurring decimals (e.g., 1/3 -> '0.(3)').",
    },
    {
        "name": "excel_sheet_column_title",
        "description": "Converts an integer to an Excel column title (1 -> A, 27 -> AA).",
    },
    {
        "name": "excel_sheet_column_number",
        "description": "Converts an Excel column title to an integer.",
    },
    {
        "name": "factorial_trailing_zeroes",
        "description": "Finds the number of trailing zeroes in 'n!'.",
    },
    {
        "name": ".generate_pascal_triangle",
        "description": "Generates Pascal's triangle up to 'num_rows'.",
    },
    {
        "name": "is_ugly_number",
        "description": "Checks if a number's prime factors are only 2, 3, or 5.",
    },
    {
        "name": "integer_to_english_words",
        "description": "Converts a non-negative integer to its English word representation.",
    },
    {
        "name": "find_missing_positive",
        "description": "Finds the smallest missing positive integer in an unsorted array.",
    },
    {
        "name": "multiply_strings",
        "description": "Multiplies two large numbers represented as strings.",
    },
    {
        "name": "plus_one",
        "description": "Adds one to a large integer represented as a list of digits.",
    },
    {
        "name": "validate_email_complex_re",
        "description": "Validates an email using a complex (but not perfect) regex.",
    },
    {
        "name": "parse_apache_log_line",
        "description": "Uses 're.match' with a complex pattern to parse a single Apache log line into a dict.",
    },
    {
        "name": "find_all_markdown_links",
        "description": "Uses 're.findall' to extract '(text, url)' tuples from markdown links '[text](url)'.",
    },
    {
        "name": "re_dos_vulnerable",
        "description": "Applies a potentially vulnerable regex (e.g., '(a+)+b') to text, good for finding catastrophic backtracking.",
    },
    {
        "name": "split_by_multiple_delimiters",
        "description": "Splits a string by a list of delimiters using 're.split'.",
    },
    {
        "name": "parse_xml_and_find_elements",
        "description": "Parses an XML string and finds all elements with a given tag.",
    },
    {
        "name": "xpath_search_xml",
        "description": "Parses XML and performs a simple XPath search.",
    },
    {
        "name": "parse_ambiguous_datetime",
        "description": "Tries to parse a datetime string that could be in one of several formats.",
    },
    {
        "name": "calculate_date_diff",
        "description": "Parses two dates in a given format and finds the difference in days.",
    },
    {
        "name": "convert_timezone_from_str",
        "description": "Parses a datetime and converts it between timezone strings (e.g., 'UTC' to 'America/New_York').",
    },
    {
        "name": "parse_url_and_extract_params",
        "description": "Uses 'urlparse' and 'parse_qs' to extract query parameters from a URL.",
    },
    {
        "name": "normalize_url",
        "description": "Cleans up a URL (removes '..', default ports, fragments).",
    },
    {
        "name": "safe_base64_decode",
        "description": "Decodes a base64 string, handling padding errors and invalid characters.",
    },
    {
        "name": "generate_text_diff",
        "description": "Generates a unified diff between two strings using 'difflib'.",
    },
    {
        "name": "wrap_text",
        "description": "Wraps text to a specified width using 'textwrap', handling long words and newlines.",
    },
    {
        "name": "parse_simple_csv_line",
        "description": "A function to parse a single CSV line, handling quoted fields and commas inside quotes (simulating 'csv').",
    },
    {
        "name": "match_filename_glob",
        "description": "Uses 'fnmatch.fnmatch' to check if a filename matches a glob pattern.",
    },
    {
        "name": "get_month_calendar_html",
        "description": "Uses the 'calendar' module to generate an HTML calendar for a given month and year.",
    },
    {
        "name": "tokenize_with_context",
        "description": "Tokenizes text with context-aware rules (nested delimiters, escape sequences, quote handling).",
    },
    {
        "name": "normalize_unicode_variants",
        "description": "Normalizes text handling multiple unicode forms, homoglyphs, and bidirectional text.",
    },
]
