# VishAgent - AI Assistant Model Documentation

**Author:** Vishnu Kiran M (ViKi Pedia)  
**Expertise:** Designing AI Solutions

---

## Table of Contents
- [Model Architecture](#model-architecture)
- [Pydantic BaseModel Overview](#pydantic-basemodel-overview)
- [ConfigDict Explained](#configdict-explained)
- [C# .NET Comparison](#c-net-comparison)
- [Installation](#installation)

---

## Model Architecture

This project uses a **hierarchical base model pattern** for consistent request/response handling across all API endpoints.

### Base Model Hierarchy

```
ItemBase (Abstract)
    ├── Message: str | None
    ├── IsInvalid: bool
    ├── model_config: ConfigDict
    │
    ├── RequestBase (Abstract)
    │       └── [All API Request Models]
    │
    └── ResponseBase (Abstract)
            └── [All API Response Models]
```

### Code Example

```python
from pydantic import BaseModel, ConfigDict, EmailStr
from typing import Optional

class ItemBase(BaseModel):
    """
    Abstract base model for all request/response models.
    
    Attributes:
        Message (str | None): Optional message field for responses/errors
        IsInvalid (bool): Flag indicating if the item failed validation
    """
    __abstract__ = True
    
    Message: str | None = None
    IsInvalid: bool = False
    
    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        validate_default=True,
        validate_assignment=True,
        arbitrary_types_allowed=False,
        str_strip_whitespace=True
    )

class RequestBase(ItemBase):
    """Base class for all API request models."""
    __abstract__ = True

class ResponseBase(ItemBase):
    """Base class for all API response models."""
    __abstract__ = True
```

---

## Pydantic BaseModel Overview

### What is Pydantic BaseModel?

**Pydantic BaseModel** is Python's equivalent to C#'s data classes with built-in validation, serialization, and deserialization.

### Key Features

| Feature | Description |
|---------|-------------|
| **Type Validation** | Automatically validates data types at runtime |
| **Data Parsing** | Converts JSON/dict to Python objects automatically |
| **Serialization** | Exports models to JSON, dict, or other formats |
| **Field Validation** | Custom validators for business logic |
| **IDE Support** | Full autocomplete and type checking |

### Why Use BaseModel?

1. **Runtime Type Safety** - Python is dynamically typed, BaseModel adds runtime type checking
2. **Automatic Validation** - No need to write manual validation code
3. **JSON Compatibility** - Seamless FastAPI integration for REST APIs
4. **Documentation** - Auto-generates OpenAPI/Swagger documentation
5. **Immutability Options** - Can enforce immutable models when needed

---

## ConfigDict Explained

### What is ConfigDict?

`ConfigDict` is Pydantic v2's configuration system that controls **how your model behaves** during validation, serialization, and deserialization.

### Why ConfigDict?

Without ConfigDict, you'd need to manually handle:
- Field name mapping (snake_case ↔ camelCase)
- Enum serialization
- Whitespace trimming
- Validation timing

**ConfigDict centralizes all model behavior configuration in one place.**

### ConfigDict Parameters Explained

```python
model_config = ConfigDict(
    # Allow population by field name
    populate_by_name=True,  
    # ✅ Allows: UserRequest(name="John") AND UserRequest(**{"name": "John"})
    
    # Use enum values instead of enum objects
    use_enum_values=True,
    # ✅ Serializes: "active" instead of <Status.ACTIVE: "active">
    
    # Validate default values
    validate_default=True,
    # ✅ Ensures: Default values also pass validation rules
    
    # Validate assignments after model creation
    validate_assignment=True,
    # ✅ Validates: user.age = 150 (re-validates on assignment)
    
    # Allow arbitrary types (useful for custom types)
    arbitrary_types_allowed=False,
    # ✅ Safety: Only allows Pydantic-compatible types
    
    # Strip whitespace from strings
    str_strip_whitespace=True
    # ✅ Auto-cleans: "  John  " becomes "John"
)
```

### Common ConfigDict Use Cases

| Configuration | Use Case |
|--------------|----------|
| `populate_by_name=True` | Support both `user_id` and `userId` field names |
| `use_enum_values=True` | Serialize enums as strings/ints, not objects |
| `validate_assignment=True` | Catch bugs when modifying model after creation |
| `str_strip_whitespace=True` | Clean user input automatically |
| `frozen=True` | Make model immutable (like C# records) |

---

## C# .NET Comparison

### Pydantic vs C# Data Models

#### **Pydantic (Python)**

```python
from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional

class ItemBase(BaseModel):
    __abstract__ = True
    Message: str | None = None
    IsInvalid: bool = False
    
    model_config = ConfigDict(
        validate_assignment=True,
        str_strip_whitespace=True
    )

class UserRequest(ItemBase):
    name: str
    email: EmailStr
    age: Optional[int] = None
    
# Usage
user = UserRequest(name="  John  ", email="john@example.com", age=30)
print(user.name)  # "John" (whitespace stripped)
user.age = 150    # ✅ Validated automatically
```

#### **C# .NET Equivalent**

```csharp
using System.ComponentModel.DataAnnotations;
using FluentValidation;

// Base Class
public abstract class ItemBase
{
    public string? Message { get; set; }
    public bool IsInvalid { get; set; } = false;
}

// Request Class
public class UserRequest : ItemBase
{
    [Required]
    [StringLength(100)]
    public string Name { get; set; }
    
    [Required]
    [EmailAddress]
    public string Email { get; set; }
    
    [Range(0, 120)]
    public int? Age { get; set; }
}

// FluentValidation (similar to ConfigDict)
public class UserRequestValidator : AbstractValidator<UserRequest>
{
    public UserRequestValidator()
    {
        RuleFor(x => x.Name)
            .NotEmpty()
            .WithMessage("Name is required")
            .Transform(x => x?.Trim()); // Strip whitespace
            
        RuleFor(x => x.Email)
            .NotEmpty()
            .EmailAddress();
            
        RuleFor(x => x.Age)
            .InclusiveBetween(0, 120)
            .When(x => x.Age.HasValue);
    }
}

// Usage in Controller
[ApiController]
[Route("api/[controller]")]
public class UserController : ControllerBase
{
    private readonly IValidator<UserRequest> _validator;
    
    [HttpPost]
    public IActionResult CreateUser([FromBody] UserRequest request)
    {
        var validationResult = _validator.Validate(request);
        if (!validationResult.IsValid)
        {
            return BadRequest(validationResult.Errors);
        }
        // Process request...
    }
}
```

### Key Differences

| Feature | Pydantic (Python) | C# .NET |
|---------|------------------|---------|
| **Validation Trigger** | Automatic on object creation | Manual validation call required |
| **Configuration** | `ConfigDict` centralized | Attributes + FluentValidation |
| **Type Checking** | Runtime only | Compile-time + Runtime |
| **Whitespace Trimming** | `str_strip_whitespace=True` | Manual with `.Transform()` |
| **Assignment Validation** | `validate_assignment=True` | Not available (need custom setters) |
| **JSON Serialization** | Built-in `.model_dump_json()` | `JsonSerializer.Serialize()` or Newtonsoft |

### ConfigDict = C# Fluent Validation + Data Annotations

```python
# Pydantic ConfigDict (All-in-one)
model_config = ConfigDict(
    validate_assignment=True,      # C#: Property setters with validation
    str_strip_whitespace=True,     # C#: .Transform(x => x.Trim())
    use_enum_values=True,          # C#: [JsonConverter(typeof(StringEnumConverter))]
    populate_by_name=True          # C#: [JsonProperty("alternate_name")]
)
```

---

## Installation

### Required Packages

```bash
# Core Pydantic with validation
pip install pydantic>=2.0.0

# Email validation support (for EmailStr)
pip install email-validator

# Complete installation
pip install -r requirements.txt
```

### requirements.txt

```txt
fastapi==0.111.0
uvicorn[standard]==0.30.1
pydantic>=2.0.0
email-validator
```

---

## Usage Examples

### Creating Request/Response Models

```python
from app.models.common.common_base import RequestBase, ResponseBase
from pydantic import EmailStr
from typing import Optional

# Define Request Model
class CreateUserRequest(RequestBase):
    name: str
    email: EmailStr
    age: Optional[int] = None

# Define Response Model
class CreateUserResponse(ResponseBase):
    user_id: int
    name: str
    email: EmailStr
    created_at: str

# Use in FastAPI endpoint
from fastapi import APIRouter

router = APIRouter()

@router.post("/users", response_model=CreateUserResponse)
def create_user(request: CreateUserRequest):
    # Validation happens automatically!
    # request.name is already trimmed
    # request.email is validated as proper email
    
    if request.age and request.age > 120:
        return CreateUserResponse(
            IsInvalid=True,
            Message="Age must be less than 120",
            user_id=0,
            name="",
            email="",
            created_at=""
        )
    
    # Process request...
    return CreateUserResponse(
        user_id=123,
        name=request.name,
        email=request.email,
        created_at="2026-01-08T10:30:00Z"
    )
```

---

## Best Practices

1. **Always inherit from RequestBase/ResponseBase** - Ensures consistent error handling
2. **Use EmailStr for email fields** - Automatic validation
3. **Enable `validate_assignment=True`** - Catch bugs early
4. **Use `str_strip_whitespace=True`** - Clean user input
5. **Document your models** - Add docstrings for API documentation
6. **Keep base models abstract** - Use `__abstract__ = True`

---

## References

- [Pydantic Documentation](https://docs.pydantic.dev/)
- [FastAPI Best Practices](https://fastapi.tiangolo.com/tutorial/body-nested-models/)
- [ConfigDict API Reference](https://docs.pydantic.dev/latest/api/config/)

---

**© 2026 Vishnu Kiran M (ViKi Pedia) - AI Solutions Expert**
 