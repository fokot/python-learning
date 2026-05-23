import functools
import inspect
import time
import dis

def timed(func, *args, **kwargs):
    # This is here so that function has it's origninal name and not wrapper
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"{func.__name__} time taken: {end - start}")
        return result
    # also this can be used
    # wrapper.__name__ = f"wrapped_{func.__name__}"
    return wrapper

@timed
def for_loop(n: int):
    my_list = []
    for i in range(n):
        my_list.append(i)
    return my_list

@timed
def list_comprehension(n: int):
    return [i for i in range(n)]


def main():
    for_loop(1000000)
    list_comprehension(1000000)
    print(for_loop.__name__)
    print(inspect.cleandoc("""
    list_comprehension is faster than for_loop because
    it has less instructions in bytecode in the loop
    """))
    print('for_loop')
    dis.dis(for_loop)
    print('list_comprehension')
    dis.dis(list_comprehension)

if __name__ == "__main__":
    main()
