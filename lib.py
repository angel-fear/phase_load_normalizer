def get_max_and_min_per_phase(sum_a: float, sum_b: float, sum_c: float) -> tuple:
    """Returns tuple of max and min values"""
    max_in = max(sum_a, sum_b, sum_c)
    min_in = min(sum_a, sum_b, sum_c)
    return max_in, min_in


def get_sum_per_phase(load_a: list, load_b: list, load_c: list) -> tuple:
    """Returns tuple of sums of accepted lists"""
    sum_a = sum(load_a)
    sum_b = sum(load_b)
    sum_c = sum(load_c)
    return sum_a, sum_b, sum_c


def move_load_to_min_loaded_phase(load_a: list, load_b: list, load_c: list, load_init: list):
    """Moves load to minimum loaded phase"""
    sum_a, sum_b, sum_c = get_sum_per_phase(load_a, load_b, load_c)
    if sum_a <= sum_b and sum_a <= sum_c and sum(load_init):
        tmp = load_init.index(max(load_init))
        load_a[tmp] = (load_init[tmp])
        load_init[tmp] = 0


def swap_two_loads(x: list, y: list, i: int):
    """Swaps two neighboring values between two lists"""
    x[i] = y[i]
    y[i] = 0
    y[i + 1] = x[i + 1]
    x[i + 1] = 0


def flip_near_phase(load_a: list, load_b: list, load_c: list, k: int):
    """Swaps two (no equal zero) values between k and k+1 position in A/B/C phases"""
    if load_a[k] != 0:
        if load_b[k + 1] != 0:
            swap_two_loads(load_b, load_a, k)
        elif load_c[k + 1] != 0:
            swap_two_loads(load_c, load_a, k)
    elif load_b[k] != 0:
        if load_a[k + 1] != 0:
            swap_two_loads(load_a, load_b, k)
        elif load_c[k + 1] != 0:
            swap_two_loads(load_c, load_b, k)
    elif load_c[k] != 0:
        if load_a[k + 1] != 0:
            swap_two_loads(load_a, load_c, k)
        elif load_b[k + 1] != 0:
            swap_two_loads(load_b, load_c, k)


def restore(x: list, in_input: list, n: int):
    """Restore sequence in X in accordance with initial Input"""
    tmp = list(x)
    x = [0] * n
    for i in range(n):
        for j in range(n):
            if tmp[i] == 0:
                continue
            if tmp[i] == in_input[j]:
                x[j] = tmp[i]
                in_input[j] = 0
                break


def phase_name_maker(load_a: list, load_b: list, load_c: list, n: int) -> list:
    """Creates list of phases names in the order of input lists"""
    phase_list = [''] * n
    for i in range(n):
        if load_a[i]:
            phase_list[i] = "A"
        if load_b[i]:
            phase_list[i] = "B"
        if load_c[i]:
            phase_list[i] = "C"
    return phase_list
