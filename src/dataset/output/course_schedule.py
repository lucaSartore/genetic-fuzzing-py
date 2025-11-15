# necessary imports (use only the python standard libraries)
from collections import deque
from collections import defaultdict

# you can define other auxiliary functions

def course_schedule(prerequisites: list[list[str]]) -> bool:
    """
    Checks if all courses can be finished, given '[course, prereq]' pairs.
    This function determines if a valid order of courses can be taken by
    performing a topological sort using Kahn's algorithm. If a cycle is
    detected in the prerequisites, it means some courses depend on each
    other in a circular fashion, making it impossible to finish all of them.

    Args:
        prerequisites: A list of course prerequisite pairs. Each inner list
                       [course_to_take, prereq_for_course] means that
                       'prereq_for_course' must be completed before
                       'course_to_take'.

    Returns:
        True if it's possible to finish all courses (i.e., no circular
        dependencies exist), False otherwise.
    """
    
    # 1. Initialize graph, in-degrees, and gather all unique courses.
    # The graph will store an adjacency list: prereq -> [list of courses that require this prereq]
    graph: dict[str, list[str]] = defaultdict(list)
    
    # in_degrees will store the count of prerequisites for each course
    in_degrees: dict[str, int] = defaultdict(int)
    
    # all_courses will keep track of every unique course mentioned,
    # both as a course to take and as a prerequisite.
    all_courses: set[str] = set()

    for course_to_take, prereq_for_course in prerequisites:
        # An edge from prereq_for_course to course_to_take indicates
        # that prereq_for_course must be completed before course_to_take.
        graph[prereq_for_course].append(course_to_take)
        
        # Increment the in-degree for course_to_take, as it has prereq_for_course
        # as one of its prerequisites.
        in_degrees[course_to_take] += 1
        
        # Add both courses to our set of all unique courses.
        all_courses.add(course_to_take)
        all_courses.add(prereq_for_course)

    # If there are no courses or prerequisites listed, it means there's nothing
    # to finish, so it's vacuously true that all can be finished.
    if not all_courses:
        return True

    # 2. Initialize a queue with all courses that have an in-degree of 0.
    # These are the courses that have no prerequisites and can be taken first.
    queue: deque[str] = deque()
    for course in all_courses:
        if in_degrees[course] == 0:
            queue.append(course)

    # 3. Perform topological sort (Kahn's Algorithm).
    # We will count how many courses we are able to process.
    processed_courses_count = 0
    
    while queue:
        # Take a course that has no remaining prerequisites.
        current_course = queue.popleft()
        processed_courses_count += 1

        # For each course that had 'current_course' as a prerequisite:
        for next_course_to_take in graph[current_course]:
            # Decrement its in-degree, as one of its prerequisites (current_course)
            # has now been "completed".
            in_degrees[next_course_to_take] -= 1
            
            # If all prerequisites for 'next_course_to_take' are now met
            # (its in-degree becomes 0), add it to the queue.
            if in_degrees[next_course_to_take] == 0:
                queue.append(next_course_to_take)

    # 4. Check for cycles.
    # If a topological sort was successful, it means we were able to process
    # all unique courses. If 'processed_courses_count' is less than the total
    # number of unique courses, it implies there's a cycle in the graph,
    # and some courses could not be processed because their prerequisites
    # could never be fully met.
    return processed_courses_count == len(all_courses)

# add this ad the end of the file
EXPORT_FUNCTION = course_schedule