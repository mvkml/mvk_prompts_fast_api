# `__future__` Annotations

## What is `from __future__ import annotations`?

`from __future__ import annotations` is a Python import statement that changes how type annotations are evaluated. It was introduced in **Python 3.7** (PEP 563) and becomes the default behavior in **Python 3.11+**.

## Key Concept

When you use this import, Python treats all type annotations as **strings** instead of evaluating them at module import time. This is called **"postponed evaluation of annotations"** or **"deferred annotation evaluation"**.

## Why Use It?

### 1. **Solves Forward Reference Problems**

Without `__future__` annotations, you get errors when referencing classes that haven't been defined yet:

```python
# ❌ This FAILS in Python < 3.10
class Node:
    def __init__(self, value: int, next: Node = None):  # NameError: name 'Node' is not defined
        self.value = value
        self.next = next
```

**With `__future__` annotations:**

```python
# ✅ This WORKS
from __future__ import annotations

class Node:
    def __init__(self, value: int, next: Node = None):  # Works! Annotation stored as string
        self.value = value
        self.next = next
```

### 2. **Enables Circular Dependencies**

```python
from __future__ import annotations

class Parent:
    def __init__(self):
        self.children: list[Child] = []  # Forward reference to Child

class Child:
    def __init__(self, parent: Parent):  # Reference back to Parent
        self.parent = parent
```

### 3. **Improves Import Performance**

Type annotations don't need to be evaluated at import time, making module loading faster:

```python
from __future__ import annotations
from typing import TYPE_CHECKING

# Only import expensive modules for type checking, not runtime
if TYPE_CHECKING:
    import pandas as pd
    import numpy as np

def process_data(df: pd.DataFrame) -> np.ndarray:  # No runtime import needed
    pass
```

### 4. **Cleaner Generic Type Hints (Python 3.9+)**

```python
from __future__ import annotations

# ✅ Use built-in types directly
def get_items() -> list[str]:  # Instead of typing.List[str]
    return ["a", "b", "c"]

def get_mapping() -> dict[str, int]:  # Instead of typing.Dict[str, int]
    return {"a": 1, "b": 2}

class Container:
    items: list[str]  # Clean syntax
```

## Before vs After Comparison

### Without `__future__` annotations (Python < 3.10)

```python
from typing import List, Dict, Optional

class UserService:
    def get_user(self, user_id: int) -> Optional['User']:  # Need quotes for forward ref
        pass

class User:
    friends: List['User']  # Need quotes
    metadata: Dict[str, str]  # Need typing.Dict
```

### With `__future__` annotations

```python
from __future__ import annotations

class UserService:
    def get_user(self, user_id: int) -> User | None:  # No quotes needed!
        pass

class User:
    friends: list[User]  # No quotes, no typing.List
    metadata: dict[str, str]  # Built-in dict works
```

## How It Works

### Without `__future__` annotations:

```python
def greet(name: str) -> str:  # Evaluates str at import time
    return f"Hello, {name}"

print(greet.__annotations__)
# Output: {'name': <class 'str'>, 'return': <class 'str'>}
```

### With `__future__` annotations:

```python
from __future__ import annotations

def greet(name: str) -> str:  # Stores as string, not evaluated
    return f"Hello, {name}"

print(greet.__annotations__)
# Output: {'name': 'str', 'return': 'str'}  # Strings!
```

## Real-World Examples

### Example 1: Pydantic Models (Common in FastAPI)

```python
from __future__ import annotations
from pydantic import BaseModel

class User(BaseModel):
    id: int
    name: str
    friends: list[User] = []  # Self-reference works!
    
class Post(BaseModel):
    id: int
    author: User
    comments: list[Comment] = []  # Forward reference

class Comment(BaseModel):
    id: int
    post: Post
    author: User
```

### Example 2: FastAPI Dependencies

```python
from __future__ import annotations
from fastapi import FastAPI, Depends
from pydantic import BaseModel

app = FastAPI()

class UserService:
    def get_current_user(self) -> User:  # Forward reference
        return User(id=1, name="Alice")

class User(BaseModel):
    id: int
    name: str

@app.get("/user")
def get_user(user: User = Depends(UserService.get_current_user)):
    return user
```

### Example 3: Complex Type Hints

```python
from __future__ import annotations
from typing import Protocol, TypeVar

T = TypeVar('T')

class Repository(Protocol[T]):
    def get(self, id: int) -> T | None:  # Clean union syntax
        ...
    
    def list(self) -> list[T]:  # Built-in list
        ...

class UserRepository:
    def get(self, id: int) -> User | None:
        return User(id=id)
    
    def list(self) -> list[User]:
        return []

class User:
    id: int
    name: str
```

## Important Considerations

### 1. **Runtime Access to Annotations**

Annotations become strings, so runtime type checking needs extra work:

```python
from __future__ import annotations
import typing

def process(value: int) -> str:
    return str(value)

# Annotations are strings
print(process.__annotations__)  
# {'value': 'int', 'return': 'str'}

# To evaluate them:
from typing import get_type_hints
hints = get_type_hints(process)
print(hints)
# {'value': <class 'int'>, 'return': <class 'str'>}
```

### 2. **Pydantic Compatibility**

Pydantic v2 handles this automatically, but v1 may need `update_forward_refs()`:

```python
from __future__ import annotations
from pydantic import BaseModel

class User(BaseModel):
    friends: list[User] = []

# Pydantic v1 may need:
User.update_forward_refs()  # Not needed in Pydantic v2
```

### 3. **Default Behavior in Python 3.11+**

In Python 3.11 and later, postponed evaluation is the default, but the import is still recommended for backward compatibility:

```python
# Python 3.11+ (implicit behavior)
class Node:
    next: Node  # Works without import

# But still recommended for compatibility:
from __future__ import annotations
```

## When to Use It

### ✅ Always Use When:
- Building APIs with **FastAPI** or similar frameworks
- Using **Pydantic** models with self-references
- Working with recursive data structures
- Using modern Python (3.9+) built-in generics

### ✅ Recommended For:
- Any new Python 3.7+ project
- Libraries that use type hints extensively
- Code with complex type relationships

### ⚠️ Be Careful When:
- Using runtime type inspection (need `get_type_hints()`)
- Working with older type-checking tools
- Code must run on Python < 3.7

## Best Practices

### 1. **Put it at the top of every module**

```python
from __future__ import annotations  # Always first import

import os
from typing import Protocol
from pydantic import BaseModel
```

### 2. **Use with TYPE_CHECKING for expensive imports**

```python
from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import pandas as pd  # Only imported by type checkers

def process(df: pd.DataFrame) -> None:  # No runtime import
    pass
```

### 3. **Combine with modern union syntax**

```python
from __future__ import annotations

def get_value() -> str | int | None:  # Clean unions
    return "hello"

def get_items() -> list[str | int]:  # Nested generics
    return [1, "two", 3]
```

## Common Issues and Solutions

### Issue 1: Pydantic Field Defaults

```python
from __future__ import annotations
from pydantic import BaseModel, Field

class User(BaseModel):
    # ❌ This fails - can't evaluate list at runtime
    # friends: list[User] = []
    
    # ✅ Use Field with default_factory
    friends: list[User] = Field(default_factory=list)
```

### Issue 2: Runtime Type Checking

```python
from __future__ import annotations
from typing import get_type_hints

def validate(value: int) -> bool:
    return isinstance(value, int)

# Need get_type_hints for runtime checks
hints = get_type_hints(validate)
param_type = hints['value']  # <class 'int'>
```

## Migration Guide

### From Old Style to New Style:

```python
# Old style (Python 3.7-3.9)
from typing import List, Dict, Optional, Union

def process(items: List[str]) -> Optional[Dict[str, Union[int, str]]]:
    return {"key": "value"}

# New style (with __future__ annotations)
from __future__ import annotations

def process(items: list[str]) -> dict[str, int | str] | None:
    return {"key": "value"}
```

## Summary

`from __future__ import annotations` is a **must-have** for modern Python development:

- ✅ Solves forward reference problems
- ✅ Enables cleaner syntax with built-in generics
- ✅ Improves import performance
- ✅ Essential for FastAPI/Pydantic applications
- ✅ Will be default in Python 3.11+

**Recommendation**: Add it to all your Python 3.7+ modules that use type hints.

---

**Related PEPs**:
- [PEP 563 – Postponed Evaluation of Annotations](https://peps.python.org/pep-0563/)
- [PEP 585 – Type Hinting Generics In Standard Collections](https://peps.python.org/pep-0585/)
- [PEP 604 – Allow writing union types as X | Y](https://peps.python.org/pep-0604/)
