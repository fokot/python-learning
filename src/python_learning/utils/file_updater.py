# updater = FileUpdater("notes.txt")  # ← __init__ runs here
# with updater as f:                  # ← __enter__ runs here
#     ...
#                                     # ← __exit__ runs here
class FileUpdater:
    def __init__(self, path):
        self.path = path
        self.content = ""

    def __enter__(self):
        with open(self.path) as f:
            self.content = f.read()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            with open(self.path, "w") as f:
                f.write(self.content)
        return False
