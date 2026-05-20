# Python Learning

## Running

```
uv run python -m python_learning.main
```
Or other module
```
uv run python -m python_learning.file_update_test
```

`uv run` auto-creates the venv and installs deps from `pyproject.toml`.

### Other options for running

```
# 1. Run the file directly — relative imports won't work
python3 src/python_learning/main.py

# 2. Run as a module — relative imports work, but you set PYTHONPATH
PYTHONPATH=src python3 -m python_learning.main

# 3. Install as a command (needs [project.scripts] in pyproject.toml)
pip install -e .
python-learning
```

**Differences:**
- #1 runs a script (no package context); #2 runs a module (full package context).
- #3 makes it a real CLI command like `black` or `pytest`.
- All three need a venv + deps installed manually (unlike `uv run`).

### Adding dependencies
```
uv add <package>
```
or
```
uv add --dev <dev_package>
```

### Type checking
```
uv run pyright src/
```
Also `mypy` is older alternative to `pyright`.

### Linting
```
uv run ruff check src/         # lint
uv run ruff check --fix src/   # lint + auto-fix
uv run ruff format src/        # format (like black)
```
