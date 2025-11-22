from numpy.random import f


def str_fun(
    input: str,
    action: int,
    reverse: bool,
    use_second_action: bool,
    second_action: int,
    adjacent_str: str
) -> str:

    if reverse:
        input = input[::-1]

    if action < 0:
        raise Exception("unsupported action")

    if action > 7:
        raise Exception("unsupported action")

    # action 0: identity
    if action == 0:
        return input

    # action 1: concatenation
    if action == 1:
        return input + adjacent_str

    is_number = False
    if input.isnumeric():
        is_number = True

    # action = 2: add one
    if is_number and action == 2:
        return str(int(input) + 1)

    
    match = False
    if input.find(adjacent_str) != -1:
        match = True

    if action == 3 and match:
        return adjacent_str


    if use_second_action:
        new_action = second_action
    else:
        new_action = action %3

    return str_fun(input + adjacent_str, second_action, reverse, False, 0, adjacent_str)


EXPORT_FUNCTION = str_fun
