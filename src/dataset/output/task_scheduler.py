import collections

def task_scheduler(tasks: list[str], n: int) -> int:
    """
    Schedules a list of tasks with a cooldown 'n'.

    Given a list of tasks and a non-negative integer 'n' representing the
    cooldown period, this function calculates the minimum number of time
    units required to complete all tasks.

    The cooldown 'n' means that if a task 'X' is executed at time 't',
    it cannot be executed again until 'n' other units of time have passed.
    These 'n' units can be filled by other distinct tasks or by idle time.

    The scheduling strategy is based on minimizing idle time by prioritizing
    the most frequent tasks.

    Args:
        tasks: A list of strings, where each string represents a task.
               Example: ['A', 'A', 'B', 'C', 'A']
        n: A non-negative integer representing the cooldown period.

    Returns:
        The minimum number of time units required to complete all tasks.
        Returns 0 if the tasks list is empty.
    """
    if not tasks:
        return 0

    # 1. Count the frequency of each task
    # Example: tasks = ['A', 'A', 'B', 'A'], n = 2
    # task_counts = {'A': 3, 'B': 1}
    task_counts = collections.Counter(tasks)

    # 2. Find the maximum frequency among all tasks
    # For {'A': 3, 'B': 1}, max_freq = 3
    max_freq = max(task_counts.values())

    # 3. Count how many tasks have this maximum frequency
    # For {'A': 3, 'B': 1}, num_max_freq_tasks = 1 (only 'A' has freq 3)
    # For {'A': 3, 'B': 3, 'C': 1}, num_max_freq_tasks = 2 ('A' and 'B' have freq 3)
    num_max_freq_tasks = sum(1 for freq in task_counts.values() if freq == max_freq)

    # 4. Calculate the minimum time based on the cooldown period and
    # the most frequent tasks.
    # Imagine a grid where rows represent the cycles of the most frequent tasks.
    # Each cycle takes (n + 1) time units: [Most Frequent Task] [Slot1] ... [SlotN].
    # There are (max_freq - 1) full cycles/frames that need to be filled.
    # The last row/cycle will only contain the tasks themselves,
    # specifically 'num_max_freq_tasks' tasks.
    #
    # Example: tasks = ['A','A','A','B','B','C'], n = 2
    # max_freq = 3, num_max_freq_tasks = 1
    # Frame 1: A _ _  (A at t=0)
    # Frame 2: A _ _  (A at t=3)
    # Last Row:A      (A at t=6)
    # The length of this base structure is (max_freq - 1) * (n + 1) + num_max_freq_tasks
    # (3 - 1) * (2 + 1) + 1 = 2 * 3 + 1 = 7
    # This time calculation accounts for the idle slots required by the cooldown.
    min_time_based_on_cooldown = (max_freq - 1) * (n + 1) + num_max_freq_tasks

    # 5. The total time required must also be at least the total number of tasks.
    # In some cases, if 'n' is very small (e.g., n=0) or if there are many
    # diverse tasks, there might be enough tasks to fill all cooldown slots
    # without any idle time. In such scenarios, the time taken is simply the
    # total count of tasks.
    #
    # Example: tasks = ['A', 'B', 'C'], n = 0
    # min_time_based_on_cooldown = (1 - 1) * (0 + 1) + 3 = 3
    # len(tasks) = 3. max(3, 3) = 3. Correct (ABC)
    #
    # Example: tasks = ['A', 'B', 'C', 'D', 'E'], n = 1
    # min_time_based_on_cooldown = (1 - 1) * (1 + 1) + 5 = 5
    # len(tasks) = 5. max(5, 5) = 5. Correct (ABCDE)
    total_tasks = len(tasks)

    # The final result is the maximum of these two values.
    return max(total_tasks, min_time_based_on_cooldown)

# add this ad the end of the file
EXPORT_FUNCTION = task_scheduler