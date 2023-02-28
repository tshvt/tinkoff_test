import time


# TASK №1
def execution_time(func):
    def wrapper(*args, **kwargs):
        start = time.time() * 1000
        result = func(*args, **kwargs)
        stop = time.time() * 1000
        print(f"function {func.__name__} took {stop - start} milliseconds to execute")
        return f"function result: {result}"
    return wrapper


@execution_time
def add_numbers(x: int, y: int) -> int:
    return x + y


# TASK №2
test_dict = {'a': 500, 'b': 5874, 'c': 560, 'd': 400, 'e': 5873}


def find_keys_with_max_values(x: dict):
    # Return dict with two max values
    # sorted_keys = dict(sorted(x.items(), key=lambda i: i[1], reverse=True)[:2])
    # return sorted_keys

    # Return tuple
    sorted_keys = sorted(x.items(), key=lambda i: i[1], reverse=True)

    # For key and value in tuple
    # return [sorted_keys[0], sorted_keys[1]]

    return [sorted_keys[0][0], sorted_keys[1][0]]  # Only keys
