import sys


class FibonacciByRecursion():
    # Find fibonacci by recursion
    def __init__(self):
        self.static_start = [0, 1, 1]
        self.cache = [0, 1, 1]

    def recursive(self, n):
        # Validate the value of n
        if not (isinstance(n, int) and n >= 0):
            raise ValueError(f"Positive integer number expected, got {n}")

        # Check for computed Fibonacci numbers
        if n < len(self.cache):
            return self.cache[n]
        else:
            # Compute and cache the requested Fibonacci number
            fib_number = self.recursive(n - 1) + self.recursive(n - 2)
            self.cache.append(fib_number)

        return self.cache[n]

    def non_resursive(self, n):
        if n < len(self.cache):
            result = self.cache[n]
            return result
        looped_cache = []
        i = 4
        last1 = 1
        last2 = 1
        while i <= n+1:
            result = last1 + last2
            if result >= sys.maxsize:
                raise ValueError(
                    f"Fibonacci value of input {n+1} is larger than max int")
            last2 = last1
            last1 = result
            looped_cache.append(result)
            i += 1
        self.cache = self.static_start+looped_cache
        return result


class FibonacciNoRecursion():
    def __init__(self):
        self.cache = [0, 1, 1]

    def __call__(self, n):
        if n < len(self.cache):
            result = self.cache[n]
            return result
        i = 4
        last1 = 1
        last2 = 1
        while i <= n+1:
            result = last1 + last2
            last2 = last1
            last1 = result
            i += 1
        return result


class Blacklist():
    def __init__(self):
        self.cache = []

    def add(self, n):
        if n not in self.cache:
            self.cache.append(n)
        return self.cache

    def remove(self, n):
        if n in self.cache:
            self.cache.remove(n)
        else:
            raise ValueError(f"Value {n} not found in blacklist")
        return self.cache
