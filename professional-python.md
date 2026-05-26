# Python for a Scala dev — starting points (job codebase)

Coming from Scala, focus learning on these.

---

## Environments and virtual environments

**Environment** = a Python interpreter + the packages installed against it. By default there's one global environment per Python install.

**Virtual environment (venv)** = a project-local, isolated copy of that setup, usually in `.venv/`. The Scala analog is closer to sbt/mill resolving dependencies per project — except in Python, packages live in a folder you activate rather than a build-tool cache.

Why they exist:
- **Dependency conflicts** — Project A needs `requests==2.20`, Project B needs `requests==2.31`. No venvs → only one can win.
- **Reproducibility** — `pip freeze > requirements.txt` (or `uv.lock`) captures exactly what's in *this* venv.
- **System protection** — macOS/Linux ship a system Python the OS depends on; installing globally can break it. Modern Python often refuses global `pip install` for this reason.
- **Cleanup** — delete `.venv/` and the project's deps are gone. No global leftover state.

Manual workflow (rarely needed today):
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
deactivate
```

In practice, use `uv` (this repo) / `poetry` / `pipenv` — they create and manage the venv for you. `uv run pytest` runs inside the project's venv without manual activation.

### What's inside `.venv/`

A venv is just a directory. Three pieces matter:

**1. `pyvenv.cfg`** — the marker file. When you run `.venv/bin/python`, Python reads this and learns where the base interpreter lives and whether to see global packages:
```
home = /opt/homebrew/opt/python@3.14/bin   ← real Python lives here
include-system-site-packages = false        ← don't see global packages
```

**2. `bin/python`** — a symlink (or tiny launcher) to the system Python. The trick: it's the *path Python is invoked from* that makes it a "venv Python." Same binary, different `sys.prefix`. `bin/` also holds the activation scripts (`activate`, `activate.fish`, …) and entry scripts for installed tools (`ruff`, `pyright`, …). On Windows it's `Scripts/` instead of `bin/`.

**3. `lib/python3.14/site-packages/`** — where `pip install` / `uv add` actually drops packages. Each venv has its own, which is the whole point: project A and project B can have different versions of `requests` without conflict.

### What "activating" really does

`source .venv/bin/activate` just prepends `.venv/bin/` to your `$PATH` and sets `$VIRTUAL_ENV`. That's it. After activation, typing `python` finds `.venv/bin/python` first, which then resolves its own `site-packages`.

You can skip activation entirely by calling `.venv/bin/python` directly — same result. This is what `uv run` does under the hood.

---

## Pass vs. Ellipsis
`pass` is a no-op statement.
`...` is an expression evaluating to the `Ellipsis` singleton (not `None`) whose value is discarded when used as a statement.
So both work as a function body but mean different things.

---

## Working with `None`

`None` is Python's null — a singleton of type `NoneType`. There's only ever one `None`.

**Non-null is the default in the type system:**
```python
x: int = 5           # cannot be None — mypy errors if you try
y: int | None = 5    # explicitly nullable (your Option[Int])
y = None             # ok
```
In mypy strict mode, if a variable isn't `| None`, it's guaranteed non-None.

**Checking:**
```python
if x is None: ...        # idiomatic — use `is`, not `==`
if x is not None: ...
```
After an `is None` check, mypy **narrows** the type — inside the `else` branch, `x: int`, not `int | None`. Same as Scala's flow typing.

**JS-equivalent helpers:**

| JS                | Python                                                      |
|-------------------|-------------------------------------------------------------|
| `x ?? default`    | `x if x is not None else default`                           |
| `x \|\| default`  | `x or default` (also falsy on `0`/`""`/`[]`)                |
| `obj?.prop`       | no operator — `obj.prop if obj is not None else None`       |
| `obj?.method()`   | same — no `?.`                                              |
| `a?.b?.c?.d`      | painful; restructure or early-return                        |

No `?.` operator (a PEP for it was rejected). Workarounds:
```python
# Walrus + early return
if (user := get_user()) is None:
    return None
return user.profile.name

# getattr with default (attributes)
name = getattr(user, "name", "unknown")

# dict.get with default (mappings)
port = config.get("port", 8080)
```

**Deep chains (`a?.b?.c?.d`)** — idiomatic Python is `try/except`. This is the "EAFP" style (Easier to Ask Forgiveness than Permission), not a hack:
```python
try:
    value = a.b.c.d
except AttributeError:
    value = None
```

**No `.map` / `.flatMap` / `.getOrElse` on optionals.** The idioms:
```python
# .getOrElse
value = maybe_value if maybe_value is not None else default

# .map
result = f(x) if x is not None else None

# .flatMap chains — just use early returns
def lookup(id: str) -> str | None:
    user = get_user(id)
    if user is None: return None
    profile = user.profile
    if profile is None: return None
    return profile.name
```

**Gotcha:** `or` treats `0`, `""`, `[]`, `False` as falsy. If you only want to replace `None`, use `x if x is not None else default`, not `x or default`.

**Asserting non-None** (when you know better than the checker):
```python
assert x is not None     # narrows for mypy, raises at runtime if wrong
y: int = x               # now type-checks
```

---

## Type hints + mypy strict mode

Python types are **not enforced at runtime** — mypy is your compiler. Configure it strict (see `mypy.ini`).

Key syntax:
```python
x: int = 5
xs: list[int] = [1, 2]          # PEP 585: builtin generics, no `List`
m: dict[str, Any] = {}
name: str | None = None         # PEP 604: this is your Option[String]
from typing import Literal, Protocol, TypeVar, Generic

# Before Python 3.12 (October 2023), type variables were declared outside the generic class, as
# T = TypeVar("T")
class Box[T]:
    def __init__(self, v: T) -> None: self.v = v
```

Gotchas:
- Generics are **erased and nominal** — no HKT, no typeclasses, no implicits.
- `Any` silently disables checking — avoid it; prefer `object` or proper unions.

---

## asyncio — async/await model

Functions are **colored**: `async def` returns a coroutine; you must `await` it. Unlike Scala `Future`, nothing runs eagerly. A `Task` is "a coroutine scheduled on the event loop" — the eager wrapper around a lazy coroutine (`asyncio.create_task(coro)` or `asyncio.gather(...)`).

```python
import asyncio

async def fetch(url: str) -> str: ...

async def main() -> None:
    # Future.sequence equivalent:
    results = await asyncio.gather(fetch("a"), fetch("b"))
    # async resource:
    async with open_conn() as c:
        async for msg in c: ...

asyncio.run(main())             # entry point
```

Key idioms in this repo: `asyncio.gather(..., return_exceptions=True)`,
`@asynccontextmanager` for lifespans, `await websocket.receive_bytes()`.
Don't call blocking I/O (`requests.get`) inside async code — it stalls the event loop. Use `httpx.AsyncClient`.

**Concurrency, not parallelism.** One event loop, one thread — only one piece of Python code runs at a time (the GIL enforces this even with threads). `gather` keeps many awaits *in flight*; the actual parallelism happens at the OS/kernel level (sockets, disk). CPU-bound work blocks the loop. Escape hatches:

| Need                                   | Tool                                                         |
|----------------------------------------|--------------------------------------------------------------|
| Run blocking I/O inside async code     | `await asyncio.to_thread(blocking_fn, args)`                 |
| Many CPU-bound jobs                    | `multiprocessing` / `concurrent.futures.ProcessPoolExecutor` |
| One CPU-bound job from async code      | `await loop.run_in_executor(ProcessPoolExecutor(), fn)`      |
| Numerical code that releases the GIL   | numpy/torch on threads work fine, GIL drops in C-land        |

For this codebase you're doing async I/O, so the GIL is a non-issue. Revisit only if you hit CPU-bound work. (Python 3.13+ has an experimental free-threaded build that removes the GIL; ignore until it's default.)

### Internals (skip until you need them)

Event loop policies, custom loops, `loop.call_soon`, `Future` vs `Task` vs coroutine distinctions, transports/protocols — interesting but unnecessary. FastAPI + `asyncio.run` + `gather` + `async with` cover ~all of what this repo does.

---

## Pydantic v2 (BaseModel, BaseSettings)

This is your case-class + JSON + validation layer. Used everywhere for config and DTOs.

```python
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings

class TranscriptBlock(BaseModel):     # like a Scala case class
    text: str
    speaker_id: int
    confidence: float = Field(ge=0, le=1)
```

Example in [pydantic_basics.py](`src/python_learning/pydantic_basics.py`). Run it as `uv run python src/python_learning/pydantic_basics.py`.

```python
class Settings(BaseSettings):         # reads from env vars automatically
    log_level: str = "INFO"
    aws_endpoint_url: str | None = None
    fvid_required_scopes: list[str] = ["fv.transcript.ingest"]

settings = Settings()                 # validates at construction
block = TranscriptBlock.model_validate(json_dict)  # parse + validate
block.model_dump()                    # to dict; .model_dump_json() to str
```

Validation happens at construction, raising `ValidationError`. Pair with mypy via the `pydantic.mypy` plugin (already enabled).
For more look into [settings folder](src/python_learning/settings/settings.py)

---

## FastAPI — routing + dependency injection

Type hints drive validation, parsing, and OpenAPI generation. Mental model: http4s + tapir squished into one, with decorators instead of DSL.

```python
from fastapi import FastAPI, Depends, Query, WebSocket

app = FastAPI(lifespan=lifespan)

@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}

@app.websocket("/v1/ingest/{key}")
async def ingest(ws: WebSocket, key: str, token: str = Query("")) -> None:
    await ws.accept()
    data = await ws.receive_bytes()

# DI: anything you put in `Depends(...)` is resolved per-request
def current_user(token: str = Query("")) -> User: ...
@app.get("/me")
async def me(user: User = Depends(current_user)) -> User: return user
```

Path params, query params, and body come from the type signature. Pydantic models in the signature → JSON body parsed + validated.

---

## pytest + fixtures + pytest-asyncio

Test discovery is convention-based: files `test_*.py`, functions `test_*`. No class hierarchy needed.

```python
import pytest

def test_adds() -> None:
    assert 1 + 1 == 2

# Fixture = setup helper, injected by name (DI by parameter name)
@pytest.fixture
def client() -> KinesisClient:
    return KinesisClient("test-stream", "http://localhost:4566")

def test_writes(client: KinesisClient) -> None:
    client.put("hello")

# Parametrize = table-driven tests
@pytest.mark.parametrize("a,b,want", [(1,1,2), (2,3,5)])
def test_sum(a: int, b: int, want: int) -> None:
    assert a + b == want

# Async tests (pytest-asyncio with asyncio_mode = "auto" in pyproject)
async def test_async_thing() -> None:
    result = await some_async()
    assert result == "ok"
```

### Timeouts for async tests
```toml
# Globally in pyproject.toml:
[tool.pytest.ini_options]
timeout = 10
```
```python
# Annotation above individual test functions
@pytest.mark.timeout(5)
async def test_async_thing() -> None:
# Or
@pytest.mark.asyncio(timeout=5)
async def test_async_thing() -> None:
```

Also used in this repo: `syrupy` for snapshot tests, `freezegun` to pin `datetime.now()`. Run via `uv run pytest -q`.

---

## Metaclasses

`class Foo(metaclass=Meta)` lets a class customize how *other classes* are constructed. Pydantic and ORMs use them internally; you almost never write one.

Closest Scala analog: macro-generated class members. If you're tempted to write one, you probably want a decorator or `__init_subclass__` instead.

---

## Descriptors

The protocol behind `@property`, `classmethod`, ORM fields, `Field(...)` etc. — objects with `__get__`/`__set__`/`__delete__` that intercept attribute access on the owning class.

You'll *use* properties constantly:
```python
class C:
    def __init__(self, name: str = "") -> None:
        self._name = name
    # This can be accessed as c.name (field) instead of c.name() (method)
    @property
    def name(self) -> str: return self._name

    # This can be set as c.name = value (setter) instead of c.name(value) (method)
    @name.setter
    def name(self, value: str) -> None:
        self._name = value
```

### Cached properties
```python
from functools import cached_property

class User:
    @cached_property
    def profile(self) -> Profile:
        return load_from_db(self.id)   # runs once, then cached on the instance
```

---

## Other things to skip

- **`__slots__`** — memory micro-optimization. Ignore unless profiling says so.
- **Abstract Base Classes (`abc.ABC`)** — prefer `typing.Protocol` for structural typing; it's lighter and matches Scala's `trait` better mentally.
- **`functools.singledispatch`** — Python's attempt at typeclass-ish dispatch; rarely worth it over plain `if isinstance`.
- **C extensions / Cython / ctypes** — not in this repo's stack.
- **`__new__`, `__init_subclass__`, `__set_name__`** — metaprogramming hooks; same reason as metaclasses.
