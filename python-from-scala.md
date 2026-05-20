# Python for Scala Developers

Things most likely to surprise you coming from Scala.

## 1. Mutable default arguments share state across calls

The #1 Python gotcha.

```python
def append_to(item, lst=[]):
    lst.append(item)
    return lst

append_to(1)   # [1]
append_to(2)   # [1, 2]  ← !!!
```

The default `[]` is created **once** at function definition, not per call. Fix: `lst=None` and `if lst is None: lst = []`.

## 2. Everything is mutable

No `val` vs `var`. No `List` vs `mutable.ListBuffer`. There's `tuple` (immutable) and `frozenset`, that's mostly it. Pass a list to a function and it can modify it. Use `@dataclass(frozen=True)` if you want immutability.

## 3. No real expression vs statement distinction

Scala: everything is an expression. Python: `if/while/for/def` are statements — can't assign their result.

```python
x = if cond: 1 else: 2     # ✗ SyntaxError
x = 1 if cond else 2       # ✓ ternary expression
```

No equivalent of `val x = if (...) ... else ...` for blocks. You write it as a statement or use a helper function.

## 4. No tail-call optimization, ever

```python
def fact(n, acc=1):
    if n == 0: return acc
    return fact(n-1, acc*n)    # stack overflow on big n
```

Python has a hard recursion limit (~1000). Loop instead. Guido has explicitly refused TCO multiple times.

## 5. Truthiness — many things are "false"

```python
if x:    # True for: non-empty containers, non-zero numbers, non-None
         # False for: 0, 0.0, "", [], {}, set(), None, False
```

`if my_list:` checks if it's non-empty. `if my_dict:` same. Convenient but surprising — a valid empty result looks identical to `None`.

## 6. `==` vs `is`

- `==` is value equality (`__eq__`)
- `is` is identity (same object in memory)

```python
[1,2] == [1,2]   # True
[1,2] is [1,2]   # False — different objects
None == None     # True
x is None        # canonical — always use `is` for None, True, False
```

Scala `==` ≈ Python `==`. Scala `eq` ≈ Python `is`.

## 7. Closures capture by reference, not value

```python
funcs = [lambda: i for i in range(3)]
[f() for f in funcs]   # [2, 2, 2] — not [0, 1, 2]!
```

All lambdas share the same `i`, which ends at `2`. Fix: `lambda i=i: i` to capture per-iteration.

A lambda is an anonymous function. lambda: i is a function that takes no arguments and returns i.
  
General syntax:
lambda <args>: <expression>

Three parts: the keyword lambda, the arguments (before :), the expression to return (after :). Whatever
the expression evaluates to, that's the return value.

Examples:
```
f = lambda: 42              # no args, returns 42
f()                         # 42

g = lambda x: x + 1         # one arg
g(5)                        # 6

h = lambda x, y: x * y      # two args
h(3, 4)                     # 12

z = lambda x, y=10: x + y   # default value
z(1)                        # 11
```

## 8. No method overloading

```python
def foo(x: int): ...
def foo(x: str): ...     # overwrites the first one
```

Only the last definition wins. Use `@singledispatch` or `if isinstance(...)`.

## 9. `None` is not a real `Option`

Scala forces you to handle `Option[T]`. Python's `None` is just a value of any type — `Optional[int]` is just `int | None` and the type checker reminds you, but at runtime nothing stops you from forgetting. Bugs slip through.

## 10. Late binding everywhere

Functions, classes, modules — all looked up by name at call time. Monkey-patching is trivial:

```python
import math
math.pi = 4    # actually works
```

Powerful, but means refactoring is risky without a type checker.

## 11. `for/while/try` have an `else` clause

```python
for x in items:
    if found(x): break
else:
    print("not found")    # runs only if loop didn't break
```

Almost no one uses this. You'll see it once and be confused.

## 12. Iterators are single-use

```python
gen = (x*2 for x in range(3))
list(gen)   # [0, 2, 4]
list(gen)   # []  — exhausted!
```

Unlike Scala's `Iterator` (also single-use) but also unlike `LazyList`. Lists/tuples are re-iterable; generators are not.

## 13. Pattern matching exists but is new and limited

`match/case` (3.10+) is structurally similar to Scala but feels less mature. No exhaustiveness checking from the language itself (pyright can do it). No guards-with-multiple-extractors. Less powerful for ADTs.

## 14. No proper sum types / sealed traits

The Scala equivalent of `sealed trait Result; case class Ok(...); case class Err(...)` is awkward in Python. Closest is:

```python
type Result = Ok | Err   # Python 3.12+ syntax
```

But there's no exhaustiveness checking unless your type checker is strict.

## 15. Indentation is syntax

You knew this, but: a stray tab vs spaces will crash. Editors usually save you, but copy-pasting between editors can corrupt files invisibly. Always use 4 spaces.

## 16. No real privacy

`_name` is "please don't touch" (convention). `__name` triggers name mangling but is still accessible. There is no `private`. Everyone can poke at everything.

## 17. `self` is explicit

Every method takes `self` as the first parameter. Forget it and you get baffling errors. Also `@classmethod`/`@staticmethod` decorators if you don't want `self`.

## 18. Classes are objects too

```python
class Foo: pass
Foo.bar = 42         # add an attribute at runtime
Foo = "no longer a class"   # rebind the name
```

Reflection is unrestricted. Tools like dependency injection or ORMs lean on this heavily.

## 19. The GIL

Threads exist but only one runs Python bytecode at a time. CPU-bound parallelism needs `multiprocessing` or external libs (numpy, etc., which release the GIL). Async (`asyncio`) handles I/O concurrency. Python 3.13+ has experimental "no-GIL" mode but it's not the default.

## 20. Imports are statements that execute code

```python
import expensive_module   # runs all top-level code in that file
```

Side effects in modules happen on import. Circular imports are messy. The whole `src/` layout / build backend setup is downstream of this design.

## Bottom line

Python is duck-typed, mutation-heavy, late-binding, and trusts you. Scala is type-safe, immutable-by-default, and constrains you. The biggest mental shift is **letting go of type-system guarantees and relying on tests + a strict type checker (pyright) instead**.
