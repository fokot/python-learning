# Protocols are used for structural typing
from typing import Protocol

class Drawable(Protocol):
    def draw(self) -> str: ...

class Circle:                 # does NOT inherit Drawable
    def draw(self) -> str:
        return "○"

class Cross:                 # does NOT inherit Drawable
    def draw(self) -> str:
        return "x"

def render(thing: Drawable) -> str:
    return thing.draw()

def main() -> None:
    shapes = [Circle(), Cross(), Circle()]
    for shape in shapes:
        print(render(shape))

if __name__ == "__main__":
    main()
