cache = {0: 0, 1: 1}


def fibonacci_of_func(n):
    if n in cache:  # Base case
        return cache[n]
        # Compute and cache the Fibonacci number
    cache[n] = fibonacci_of_func(
        n - 1) + fibonacci_of_func(n - 2)  # Recursive case
    return cache[n]
