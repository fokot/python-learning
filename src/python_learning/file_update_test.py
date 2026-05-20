from python_learning.utils.file_updater import FileUpdater, file_number_updater


def main():
    print("Hello from python-learning!")
    with FileUpdater("test.txt") as f:
        print(f"Content is: {f.content}")
        number = int(f.content)
        f.content = str(number + 1)
        print(f"New content: {f.content}")

    with file_number_updater("test.txt") as number:
        print(f"Number is: {number.value}")
        number.value += 1
        print(f"New number: {number.value}")


if __name__ == "__main__":
    main()
