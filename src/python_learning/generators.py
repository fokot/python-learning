from .list_comprehensions import timed

@timed
def loop(n: int) -> int:
    result = 0
    for i in range(n):
        for r in range(2):
            result += i * r
    return result

@timed
def generator(n: int) -> int:
    return sum(i * r for i in range(n) for r in range(2))

def main():
    print(loop(30))
    print(generator(30))

if __name__ == "__main__":
    main()
