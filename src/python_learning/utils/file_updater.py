# updater = FileUpdater("notes.txt")  # ← __init__ runs here
# with updater as f:                  # ← __enter__ runs here
#     ...
#                                     # ← __exit__ runs here
class FileUpdater:
    def __init__(self, path):
        self.path = path
        self.content = ""

    def __enter__(self):
        try:
            with open(self.path) as f:
                self.content = f.read()
        except FileNotFoundError:
            self.content = "0"
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            with open(self.path, "w") as f:
                f.write(self.content)
        return False

from contextlib import contextmanager
from dataclasses import dataclass
from typing import Generator, Self

# Without @dataclass — manually written:
# class FileNumber:
#     def __init__(self, value):
#         self.value = value

#     def __repr__(self):
#         return f"FileNumber(value={self.value!r})"

#     def __eq__(self, other):
#         if not isinstance(other, FileNumber):
#             return NotImplemented
#         return self.value == other.value
@dataclass
class FileNumber:
    value: int

@contextmanager
def file_number_updater(path: str) -> Generator[FileNumber, None, None]:
    try:
        with open(path) as f:
            wrapper = FileNumber(int(f.read().strip()))
    except FileNotFoundError:
        wrapper = FileNumber(0)
    yield wrapper
    with open(path, "w") as f:
        f.write(str(wrapper.value))
