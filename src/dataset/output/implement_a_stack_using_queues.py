# necessary imports (use only the python standard libraries)
import collections
from typing import Any, Deque

# you can define other auxiliary functions
class StackUsingTwoQueues:
    """
    Implements a Last-In, First-Out (LIFO) stack data structure
    using two collections.deque objects (queues).

    This implementation prioritizes O(1) time complexity for 'pop', 'top', and 'is_empty'
    operations, making the 'push' operation O(N) where N is the current size of the stack.

    Internal queues:
    - _q1: The primary queue. Elements are stored in stack order,
           meaning the top element of the stack is always at the front of _q1.
    - _q2: An auxiliary queue used during the 'push' operation for reordering elements.
    """
    def __init__(self) -> None:
        """
        Initializes an empty stack.
        """
        self._q1: Deque[Any] = collections.deque()  # Primary queue
        self._q2: Deque[Any] = collections.deque()  # Auxiliary queue

    def push(self, x: Any) -> None:
        """
        Pushes element x onto the stack.
        
        The element x becomes the new top of the stack.
        Time complexity: O(N), where N is the current number of elements in the stack.
                         This is because all existing elements are moved from _q1 to _q2
                         after x is added, and then the queues are swapped.
        """
        # 1. Add the new element 'x' to the auxiliary queue (_q2).
        self._q2.append(x)
        
        # 2. Move all elements from the primary queue (_q1) to the auxiliary queue (_q2).
        #    This reorders _q2 such that 'x' is at its front, followed by the
        #    elements that were previously in _q1 (maintaining their relative order).
        while self._q1:
            self._q2.append(self._q1.popleft())
        
        # 3. Swap _q1 and _q2. Now _q1 contains all elements in stack order (top at front),
        #    and _q2 is empty, ready for the next push.
        self._q1, self._q2 = self._q2, self._q1

    def pop(self) -> Any:
        """
        Removes the element on top of the stack and returns it.
        
        Time complexity: O(1).
        Raises:
            IndexError: If the stack is empty.
        """
        if self.is_empty():
            raise IndexError("pop from empty stack")
        return self._q1.popleft() # The top element is always at the front of _q1

    def top(self) -> Any:
        """
        Returns the element on top of the stack without removing it.
        
        Time complexity: O(1).
        Raises:
            IndexError: If the stack is empty.
        """
        if self.is_empty():
            raise IndexError("top from empty stack")
        return self._q1[0] # The top element is always at the front of _q1

    def is_empty(self) -> bool:
        """
        Checks if the stack is empty.
        
        Time complexity: O(1).
        Returns:
            True if the stack contains no elements, False otherwise.
        """
        return not bool(self._q1)
    
    def size(self) -> int:
        """
        Returns the number of elements currently in the stack.
        
        Time complexity: O(1).
        Returns:
            The integer count of elements in the stack.
        """
        return len(self._q1)


def implement_a_stack_using_queues() -> StackUsingTwoQueues:
    """
    Factory function that returns a new instance of a stack simulated using two queues.
    
    The returned object provides methods for standard stack operations:
    `push(x)`: Adds an element 'x' to the top of the stack.
    `pop()`: Removes and returns the top element of the stack.
    `top()`: Returns the top element of the stack without removing it.
    `is_empty()`: Checks if the stack is empty.
    `size()`: Returns the number of elements in the stack.

    Example Usage:
    my_stack = implement_a_stack_using_queues()
    my_stack.push(10)
    my_stack.push(20)
    print(f"Stack size: {my_stack.size()}")      # Output: Stack size: 2
    print(f"Top element: {my_stack.top()}")     # Output: Top element: 20
    print(f"Popped element: {my_stack.pop()}")  # Output: Popped element: 20
    print(f"Is stack empty? {my_stack.is_empty()}") # Output: Is stack empty? False
    my_stack.push(30)
    print(f"Top element: {my_stack.top()}")     # Output: Top element: 30
    """
    return StackUsingTwoQueues()

# add this ad the end of the file
EXPORT_FUNCTION = implement_a_stack_using_queues