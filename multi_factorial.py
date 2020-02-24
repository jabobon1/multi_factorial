from time import time
from multiprocessing import Pool, cpu_count


def timer(func):
    """Decorator for counting time"""

    def wrapper(*args, **kwargs):
        t_1 = time()
        res = func(*args, **kwargs)
        print(f'Calculating factorial {func.__name__}({args[0]}) takes {time() - t_1}')
        return res

    return wrapper


@timer
def standart_factorial(factorial):
    """Calculates factorial in one process"""

    result = 1
    for num in range(1, factorial + 1):
        result *= num
    return result


def spliter(factorial: int, quantity=cpu_count()):
    """
    Splits arguments for get_range() generator by quantity

    :return: List(Tuple)
    spliter(8, 4) -> [(7, 2, 8), (7, 4, 8), (7, 6, 8), (7, 8, 8)]
    """
    return [(st, factorial, quantity * 2) for st in range(2, quantity * 2 + 1, 2)]


def get_factorial(generator_args):
    """
    Calculates factorial for one of parts
    :param generator_args: tuple, args for range generator
    :return: int
    """
    start, factorial, step = generator_args

    result = 1
    for num in range(start, factorial + 1, step):
        result *= num * (num - 1)

    # If factorial is even range won't return a last value
    # and needed calculate it only in one process which will be with start==2
    if factorial % 2 and start == 2:
        result *= factorial

    return result


@timer
def multi_factorial(factorial):
    """Calculates factorial in multi process"""

    arguments = spliter(factorial)
    with Pool() as p:
        results = p.map(get_factorial, arguments)

    # Connects all results in one
    final_res = 1
    for res in results:
        final_res *= res

    return final_res


if __name__ == '__main__':
    factorial = 100001
    pool_res = multi_factorial(factorial)
    standart_res = standart_factorial(factorial)

    print(pool_res == standart_res)
