import time
import tracemalloc


def measure_execution(func, *args):
    start = time.perf_counter()
    result = func(*args)
    end = time.perf_counter()

    return result, end - start


def measure_memory(func, *args):
    tracemalloc.start()

    result = func(*args)

    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    return result, peak

import time
import tracemalloc


def measure(func, *args):
    tracemalloc.start()

    start = time.perf_counter()
    result = func(*args)
    end = time.perf_counter()

    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    return result, end-start, peak