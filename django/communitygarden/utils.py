def clamp(val, lower, upper):
    return min(max(val, lower), upper)


def print_in_main_process(*args, **kwargs):
    print(*args, **kwargs)
