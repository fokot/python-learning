from python_learning.utils.file_updater import FileUpdater

def main():
    print("Hello from python-learning!")
    with FileUpdater("test.txt") as f:
        print(f"Content is: {f.content}")
        number = int(f.content)
        f.content = str(number + 1)
        print(f"New content: {f.content}")

if __name__ == "__main__":
    main()
