# Generics let one function work for any type while keeping type info.
# PEP 695 syntax (Python 3.12+): the [T] after the name declares a type parameter.
from collections.abc import Callable

def find[T](items: list[T], predicate: Callable[[T], bool]) -> T | None:
    for item in items:
        if predicate(item):
            return item
    return None

def main() -> None:
    numbers = [1, 2, 3, 4, 5]
    first_even = find(numbers, lambda n: n % 2 == 0)
    print(first_even)               # 2   — inferred as int | None

    words = ["hi", "hello", "hey"]
    long_word = find(words, lambda w: len(w) > 3)
    print(long_word)                # hello — inferred as str | None

    missing = find(numbers, lambda n: n > 100)
    print(missing)                  # None

if __name__ == "__main__":
    main()
