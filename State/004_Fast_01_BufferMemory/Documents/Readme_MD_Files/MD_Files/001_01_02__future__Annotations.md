# `__future__` Annotations — Reference

This note explains why and how we use `__future__` annotations in the codebase, and points to a concrete module where it is applied for easy reference.

## What it does
- Enables postponed evaluation of type annotations, treating them as strings at runtime.
- Simplifies forward references (types defined later in the file or in modules that would otherwise cause circular imports).
- Helps reduce import-time overhead and circular dependency issues in larger applications.

## How to use
Place the import at the very top of your Python module:

```python
from __future__ import annotations
```

Then you can freely use forward-referenced types without quoting or worrying about import order. Example:

```python
from dataclasses import dataclass

from __future__ import annotations

@dataclass
class Node:
	value: int
	next: Node | None  # forward reference to `Node`
```

Without `from __future__ import annotations`, you would typically need to write `"Node"` or rearrange imports/classes to avoid NameError or circular import issues.

## Where it’s used in this application
- Module: C:\v\v\learn\lv_python\ai\VishAgent\app\api\api_state\api_buffer_memory.py
- Purpose: To safely use type hints across internal APIs (including potential forward references) and keep import-time dependencies minimal.

If you’re reviewing or extending `api_buffer_memory.py`, ensure the `from __future__ import annotations` line remains at the very top of the file (above any other imports) so that annotations are postponed correctly.

## When to apply it
- You have types that reference each other (mutual or circular references).
- You want cleaner type hints without quoting names.
- You’re refactoring module boundaries and want to avoid import cycles.

## Notes
- Python 3.11 adopts PEP 649/PEP 563 behavior changes; using `from __future__ import annotations` is still a safe way to standardize postponed evaluation in mixed-version codebases.
- Keep the future import at the top of the file, with no code above it.
