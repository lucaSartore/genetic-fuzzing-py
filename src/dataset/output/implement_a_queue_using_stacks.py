# necessary imports (use only the python standard libraries)
from typing import Any, Type

# you can define other auxiliary functions

class TwoStackQueue:
    """
    A queue implementation that uses two internal stacks (Python lists)
    to simulate First-In, First-Out (FIFO) behavior.

    - `_in_stack`: Used for enqueue operations. New items are pushed here.
    - `_out_stack`: Used for dequeue and peek operations. Items are popped from here.
                    When `_out_stack` is empty, all items are transferred from `_in_stack`
                    to `_out_stack` to reverse their order.
    """

    def __init__(self) -> None:
        """
        Initializes an empty queue with two internal lists to act as stacks.
        """
        self._in_stack: list[Any] = []
        self._out_stack: list[Any] = []

    def enqueue(self, item: Any) -> None:
        """
        Adds an item to the back of the queue.
        This operation has a time complexity of O(1).
        """
        self._in_stack.append(item)

    def dequeue(self) -> Any:
        """
        Removes and returns the item from the front of the queue.
        If `_out_stack` is empty, all elements are transferred from `_in_stack` to `_out_stack`.
        Raises an `IndexError` if the queue is empty.
        This operation has an amortized time complexity of O(1). In the worst case (when
        `_out_stack` is empty and a transfer is needed), it is O(N) where N is the number
        of elements in `_in_stack`, but this cost is spread out over N `dequeue` operations.
        """
        if not self._out_stack:
            if not self._in_stack:
                raise IndexError("dequeue from empty queue")
            # Transfer all elements from in_stack to out_stack to reverse their order
            while self._in_stack:
                self._out_stack.append(self._in_stack.pop())
        return self._out_stack.pop()

    def peek(self) -> Any:
        """
        Returns the item at the front of the queue without removing it.
        If `_out_stack` is empty, elements are transferred from `_in_stack` to `_out_stack`.
        Raises an `IndexError` if the queue is empty.
        This operation has an amortized time complexity of O(1), similar to `dequeue`.
        """
        if not self._out_stack:
            if not self._in_stack:
                raise IndexError("peek from empty queue")
            # Transfer all elements from in_stack to out_stack to reverse their order
            while self._in_stack:
                self._out_stack.append(self._in_stack.pop())
        return self._out_stack[-1]  # The top of out_stack is the front of the queue

    def is_empty(self) -> bool:
        """
        Checks if the queue is empty.
        Returns `True` if the queue is empty, `False` otherwise.
        This operation has a time complexity of O(1).
        """
        return not self._in_stack and not self._out_stack

    def size(self) -> int:
        """
        Returns the number of items currently in the queue.
        This operation has a time complexity of O(1).
        """
        return len(self._in_stack) + len(self._out_stack)

    def __len__(self) -> int:
        """
        Allows the use of `len(queue_instance)` to get the queue's size.
        """
        return self.size()

    def __str__(self) -> str:
        """
        Provides a string representation of the queue, showing its logical order.
        """
        if self.is_empty():
            return "Queue([])"

        # The logical order of queue elements is:
        # 1. Elements in _out_stack, from its top (which is its end) to its bottom (its beginning).
        # 2. Elements in _in_stack, from its bottom (its beginning) to its top (its end).
        # Example: _in_stack=[1,2], _out_stack=[5,4,3] -> logical queue: [3,4,5,1,2]
        
        # `reversed(self._out_stack)` gives elements in enqueue order (front of queue first)
        # `self._in_stack` gives elements in enqueue order (back of queue last)
        queue_elements_in_order = [str(x) for x in reversed(self._out_stack)] + [str(x) for x in self._in_stack]
        return f"Queue([{', '.join(queue_elements_in_order)}])"


def implement_a_queue_using_stacks() -> TwoStackQueue:
    """
    Generates and returns an instance of a queue simulated using two stacks (Python lists).

    The returned `TwoStackQueue` object provides the standard queue interface:
    - `enqueue(item: Any) -> None`: Adds an item to the back of the queue.
    - `dequeue() -> Any`: Removes and returns the item from the front of the queue.
                          Raises `IndexError` if the queue is empty.
    - `peek() -> Any`: Returns the item at the front of the queue without removing it.
                       Raises `IndexError` if the queue is empty.
    - `is_empty() -> bool`: Checks if the queue contains any items.
    - `size() -> int`: Returns the total number of items in the queue.
    - `__len__()`: Allows using `len()` directly on the queue instance.
    - `__str__()`: Provides a human-readable string representation of the queue.

    Example Usage:
    >>> my_queue = implement_a_queue_using_stacks()
    >>> my_queue.enqueue("apple")
    >>> my_queue.enqueue("banana")
    >>> print(my_queue.size())
    2
    >>> print(my_queue.dequeue())
    apple
    >>> my_queue.enqueue("cherry")
    >>> print(my_queue.peek())
    banana
    >>> print(my_queue)
    Queue([banana, cherry])
    >>> while not my_queue.is_empty():
    ...     print(my_queue.dequeue())
    banana
    cherry
    >>> print(my_queue.is_empty())
    True
    """
    return TwoStackQueue()

# add this ad the end of the file
EXPORT_FUNCTION = implement_a_queue_using_stacks