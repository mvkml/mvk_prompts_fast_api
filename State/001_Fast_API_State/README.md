# VishAgent - Dependency Injection & Architectural Patterns

**Author**: VISHNU KIRAN M  
**Expertise**: Designing AI Solutions  
**Project**: MARVISH Industrial AI Assistant  
**Framework**: FastAPI + LangChain + LangGraph  
**Focus**: AI-powered claim policy analysis with clean architecture
(ViKi Pedia) 
---

## Table of Contents
- [Dependency Injection](#dependency-injection)
- [Different Ways of Dependency Injection](#different-ways-of-dependency-injection)
- [When to Use What](#when-to-use-what)
- [VishAgent Patterns](#vishagent-patterns)
- [Author Profile](#author-profile)

---

## Dependency Injection

### What is Dependency Injection?

**Dependency Injection (DI)** is a design pattern where objects receive their dependencies from external sources rather than creating them internally. This promotes loose coupling, testability, and maintainability.

### Core Concepts

```python
# ❌ WITHOUT Dependency Injection (Tight Coupling)
class UserService:
    def __init__(self):
        self.dal = UserDAL()  # Hard-coded dependency
        self.logger = Logger()  # Hard-coded dependency
    
    def create_user(self, user):
        # Tightly coupled to specific implementations
        self.dal.save(user)

# ✅ WITH Dependency Injection (Loose Coupling)
class UserService:
    def __init__(self, dal: UserDAL, logger: Logger):
        self.dal = dal  # Injected dependency
        self.logger = logger  # Injected dependency
    
    def create_user(self, user):
        # Can work with any implementation
        self.dal.save(user)
```

### Benefits of Dependency Injection

| Benefit | Description |
|---------|-------------|
| **Testability** | Easy to mock dependencies in unit tests |
| **Maintainability** | Change implementations without modifying code |
| **Flexibility** | Swap implementations at runtime |
| **Loose Coupling** | Components don't depend on concrete implementations |
| **Reusability** | Components can be reused with different dependencies |

---

## Different Ways of Dependency Injection

### 1. Constructor Injection (Recommended)

**Definition**: Dependencies are passed through the class constructor.

**Advantages**:
- Explicit dependencies
- Immutable after construction
- Clear required dependencies
- Best for required dependencies

**Example in VishAgent**:
```python
# services/user_service.py
class UserService:
    """Constructor Injection - Dependencies passed in __init__"""
    
    def __init__(self, dal: UserDAL, logger: Logger = None):
        """
        Constructor injection ensures dependencies are available
        before the object is used.
        
        Args:
            dal: Required dependency - Data Access Layer
            logger: Optional dependency - Logger instance
        """
        self.dal = dal
        self.logger = logger or logging.getLogger(__name__)
    
    async def create_user(self, request: UserRequest) -> UserModel:
        self.logger.info(f"Creating user: {request.email}")
        
        # Validate email doesn't exist
        existing = await self.dal.get_user_by_email(request.email)
        if existing:
            raise ValueError("Email already exists")
        
        # Create user
        user = await self.dal.create_user(request)
        self.logger.info(f"User created: {user.id}")
        return user

# Usage in endpoint
@user_router.post("/")
async def create_user(request: UserRequest) -> UserResponse:
    # Inject dependencies via constructor
    dal = UserDAL(database)
    logger = logging.getLogger(__name__)
    service = UserService(dal=dal, logger=logger)
    
    user = await service.create_user(request)
    return UserResponse(Data=user)
```

---

### 2. FastAPI Dependency Injection (Recommended for FastAPI)

**Definition**: FastAPI's built-in DI system using the `Depends()` function.

**Advantages**:
- Automatic dependency resolution
- Built-in caching within request scope
- Clean syntax
- Request-scoped lifecycle

**Example in VishAgent**:
```python
from fastapi import Depends
from typing import Annotated

# Define dependency functions
def get_database():
    """Database connection dependency"""
    db = Database()
    try:
        yield db
    finally:
        db.close()

def get_user_dal(db: Annotated[Database, Depends(get_database)]):
    """UserDAL dependency with database injection"""
    return UserDAL(db)

def get_user_service(dal: Annotated[UserDAL, Depends(get_user_dal)]):
    """UserService dependency with DAL injection"""
    return UserService(dal)

# Use in endpoint with automatic injection
@user_router.post("/")
async def create_user(
    request: UserRequest,
    service: Annotated[UserService, Depends(get_user_service)]
) -> UserResponse:
    """
    FastAPI automatically:
    1. Creates Database instance
    2. Creates UserDAL with database
    3. Creates UserService with dal
    4. Injects service into endpoint
    """
    response = UserResponse()
    try:
        user = await service.create_user(request)
        response.Data = user
        response.Message = "User created successfully"
        return response
    except ValueError as ve:
        response.IsInvalid = True
        response.Message = {"error": str(ve)}
        return response
```

**Advanced FastAPI DI with Settings**:
```python
from functools import lru_cache

@lru_cache()
def get_settings():
    """Cached settings - created once per application"""
    return Settings()

def get_openai_client(settings: Annotated[Settings, Depends(get_settings)]):
    """OpenAI client with settings injection"""
    return OpenAI(api_key=settings.open_ai_key)

@app.get("/prompt")
async def process_prompt(
    prompt: str,
    client: Annotated[OpenAI, Depends(get_openai_client)]
):
    """Endpoint with automatic OpenAI client injection"""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    return response
```

---

### 3. Property Injection (Setter Injection)

**Definition**: Dependencies are set after object creation via properties or setters.

**Advantages**:
- Optional dependencies
- Can change dependencies after construction
- Flexible

**Disadvantages**:
- Object may be in invalid state
- Harder to track required dependencies

**Example**:
```python
class UserService:
    """Property Injection - Dependencies set via properties"""
    
    def __init__(self):
        self._dal = None
        self._logger = None
    
    @property
    def dal(self) -> UserDAL:
        if self._dal is None:
            raise ValueError("DAL not set")
        return self._dal
    
    @dal.setter
    def dal(self, value: UserDAL):
        self._dal = value
    
    @property
    def logger(self) -> Logger:
        return self._logger or logging.getLogger(__name__)
    
    @logger.setter
    def logger(self, value: Logger):
        self._logger = value

# Usage
service = UserService()
service.dal = UserDAL(database)  # Property injection
service.logger = custom_logger   # Optional property injection
```

---

### 4. Method Injection

**Definition**: Dependencies are passed as parameters to methods that need them.

**Advantages**:
- Flexible per-method dependencies
- No state management
- Clear what each method needs

**Disadvantages**:
- Can clutter method signatures
- Repeated parameter passing

**Example**:
```python
class UserService:
    """Method Injection - Dependencies passed to each method"""
    
    async def create_user(
        self,
        request: UserRequest,
        dal: UserDAL,  # Injected per method call
        logger: Logger = None
    ) -> UserModel:
        """Each method receives its own dependencies"""
        logger = logger or logging.getLogger(__name__)
        logger.info(f"Creating user: {request.email}")
        
        user = await dal.create_user(request)
        return user
    
    async def get_user(
        self,
        user_id: int,
        dal: UserDAL  # Injected per method call
    ) -> Optional[UserModel]:
        """Different method, same dependency pattern"""
        return await dal.get_user_by_id(user_id)

# Usage
service = UserService()
dal = UserDAL(database)
user = await service.create_user(request, dal=dal)
```

---

### 5. Interface-Based Injection (Abstract Base Classes)

**Definition**: Inject interfaces/abstract classes rather than concrete implementations.

**Advantages**:
- Program to interfaces, not implementations
- Maximum flexibility
- Easy to swap implementations
- Ideal for testing

**Example**:
```python
from abc import ABC, abstractmethod

# Define interface
class IUserRepository(ABC):
    """User repository interface"""
    
    @abstractmethod
    async def create_user(self, user: UserRequest) -> UserModel:
        pass
    
    @abstractmethod
    async def get_user_by_id(self, user_id: int) -> Optional[UserModel]:
        pass

# Concrete implementations
class PostgresUserRepository(IUserRepository):
    """PostgreSQL implementation"""
    
    def __init__(self, connection_string: str):
        self.connection = connection_string
    
    async def create_user(self, user: UserRequest) -> UserModel:
        # PostgreSQL-specific implementation
        pass

class MongoUserRepository(IUserRepository):
    """MongoDB implementation"""
    
    def __init__(self, mongo_client):
        self.client = mongo_client
    
    async def create_user(self, user: UserRequest) -> UserModel:
        # MongoDB-specific implementation
        pass

# Service depends on interface, not concrete class
class UserService:
    def __init__(self, repository: IUserRepository):
        """Accepts any implementation of IUserRepository"""
        self.repository = repository
    
    async def create_user(self, request: UserRequest) -> UserModel:
        return await self.repository.create_user(request)

# Inject different implementations
service_postgres = UserService(PostgresUserRepository("connection_string"))
service_mongo = UserService(MongoUserRepository(mongo_client))
```

---

### 6. Container-Based Injection (Dependency Container)

**Definition**: Use a DI container/framework to manage dependencies.

**Advantages**:
- Centralized dependency management
- Automatic resolution
- Lifecycle management
- Configuration-based

**Example with dependency-injector library**:
```python
from dependency_injector import containers, providers

class Container(containers.DeclarativeContainer):
    """Dependency Injection Container"""
    
    # Configuration
    config = providers.Configuration()
    
    # Database
    database = providers.Singleton(
        Database,
        host=config.db_host,
        port=config.db_port
    )
    
    # DAL
    user_dal = providers.Factory(
        UserDAL,
        database=database
    )
    
    # Services
    user_service = providers.Factory(
        UserService,
        dal=user_dal
    )

# Setup container
container = Container()
container.config.db_host.from_value("localhost")
container.config.db_port.from_value(5432)

# Usage
service = container.user_service()
user = await service.create_user(request)
```

---

## When to Use What

### Decision Matrix

| Scenario | Recommended DI Method | Reason |
|----------|----------------------|---------|
| **FastAPI Endpoints** | FastAPI Depends() | Built-in, automatic resolution, clean |
| **Required Dependencies** | Constructor Injection | Explicit, ensures valid state |
| **Optional Dependencies** | Constructor with defaults | Clear intent, still immutable |
| **Testing** | Constructor Injection | Easy to mock |
| **Multiple Implementations** | Interface-Based | Flexibility, swappable |
| **Complex App** | Container-Based | Centralized management |
| **Per-Request Scope** | FastAPI Depends() | Request-scoped lifecycle |
| **Simple Scripts** | Direct instantiation | Overkill to use DI |

### Use Case Examples

#### Use Case 1: Simple Service (Constructor Injection)
```python
# ✅ Good for simple cases
class UserService:
    def __init__(self, dal: UserDAL):
        self.dal = dal

service = UserService(UserDAL(database))
```

#### Use Case 2: FastAPI Endpoint (FastAPI Depends)
```python
# ✅ Best for FastAPI applications
def get_user_service(dal: Annotated[UserDAL, Depends(get_dal)]):
    return UserService(dal)

@router.post("/")
async def create_user(service: Annotated[UserService, Depends(get_user_service)]):
    pass
```

#### Use Case 3: Multiple Implementations (Interface-Based)
```python
# ✅ Best when you need to swap implementations
class UserService:
    def __init__(self, repository: IUserRepository):
        self.repository = repository

# Can inject PostgreSQL, MongoDB, or any other implementation
```

#### Use Case 4: Testing (Constructor Injection + Mocks)
```python
# ✅ Easy to test with constructor injection
def test_create_user():
    # Mock dependencies
    mock_dal = Mock(spec=UserDAL)
    mock_dal.create_user.return_value = UserModel(id=1, name="Test")
    
    # Inject mocks
    service = UserService(dal=mock_dal)
    
    # Test
    result = await service.create_user(request)
    assert result.id == 1
```

---

## VishAgent Patterns

### Current Pattern: Manual Constructor Injection

```python
# api/api_mange_user/api_user.py
@user_router.post("/")
async def create_user(request: UserRequest) -> UserResponse:
    """Manual dependency injection in each endpoint"""
    response = UserResponse()
    try:
        # Manually create dependencies
        dal = UserDAL()
        service = UserService(dal)
        
        user = await service.create_user(request)
        response.Data = user
        return response
    except Exception as ex:
        response.IsInvalid = True
        response.Message = {"error": str(ex)}
        return response
```

### Recommended Pattern: FastAPI Depends

```python
# core/dependencies.py
"""Centralized dependency definitions"""

def get_database():
    """Database connection dependency"""
    db = Database(
        host=settings.db_host,
        port=settings.db_port,
        name=settings.db_name
    )
    try:
        yield db
    finally:
        db.close()

def get_user_dal(db: Annotated[Database, Depends(get_database)]):
    """UserDAL factory"""
    return UserDAL(db)

def get_user_service(dal: Annotated[UserDAL, Depends(get_user_dal)]):
    """UserService factory"""
    return UserService(dal)

# api/api_mange_user/api_user.py
@user_router.post("/")
async def create_user(
    request: UserRequest,
    service: Annotated[UserService, Depends(get_user_service)]
) -> UserResponse:
    """Clean endpoint with automatic dependency injection"""
    response = UserResponse()
    try:
        user = await service.create_user(request)
        response.Data = user
        response.Message = "User created successfully"
        return response
    except ValueError as ve:
        response.IsInvalid = True
        response.Message = {"validation_error": str(ve)}
        return response
```

### Migration Path

```python
# Step 1: Create core/dependencies.py
# Step 2: Define dependency functions
# Step 3: Update endpoints to use Depends()
# Step 4: Remove manual instantiation

# Before (Current)
dal = UserDAL()
service = UserService(dal)

# After (Recommended)
service: Annotated[UserService, Depends(get_user_service)]
```

---

## Best Practices

### 1. **Prefer Constructor Injection for Services**
```python
# ✅ Good
class UserService:
    def __init__(self, dal: UserDAL, logger: Logger = None):
        self.dal = dal
        self.logger = logger or logging.getLogger(__name__)
```

### 2. **Use FastAPI Depends() for Endpoints**
```python
# ✅ Good
@router.post("/")
async def endpoint(service: Annotated[Service, Depends(get_service)]):
    pass
```

### 3. **Provide Defaults for Optional Dependencies**
```python
# ✅ Good
class UserService:
    def __init__(self, dal: UserDAL, cache: Cache = None):
        self.dal = dal
        self.cache = cache or InMemoryCache()
```

### 4. **Use Type Hints**
```python
# ✅ Good - Clear types
def __init__(self, dal: UserDAL, logger: Logger):
    pass

# ❌ Avoid - No type information
def __init__(self, dal, logger):
    pass
```

### 5. **Keep Dependencies Minimal**
```python
# ✅ Good - Few focused dependencies
class UserService:
    def __init__(self, dal: UserDAL):
        self.dal = dal

# ❌ Avoid - Too many dependencies
class UserService:
    def __init__(self, dal, cache, logger, email, sms, analytics, ...):
        pass  # God object anti-pattern
```

### 6. **Inject Interfaces, Not Implementations**
```python
# ✅ Good - Flexible
class UserService:
    def __init__(self, repository: IUserRepository):
        pass

# ❌ Less flexible - Tied to PostgreSQL
class UserService:
    def __init__(self, postgres_dal: PostgresUserDAL):
        pass
```

---

## Testing with Dependency Injection

### Unit Testing Example

```python
import pytest
from unittest.mock import Mock, AsyncMock

@pytest.mark.asyncio
async def test_create_user_success():
    """Test user creation with mocked dependencies"""
    
    # Arrange: Create mocks
    mock_dal = Mock(spec=UserDAL)
    mock_dal.get_user_by_email = AsyncMock(return_value=None)
    mock_dal.create_user = AsyncMock(
        return_value=UserModel(id=1, name="John", email="john@example.com")
    )
    
    # Inject mocks via constructor
    service = UserService(dal=mock_dal)
    request = UserRequest(name="John", email="john@example.com")
    
    # Act: Call method
    result = await service.create_user(request)
    
    # Assert: Verify behavior
    assert result.id == 1
    assert result.name == "John"
    mock_dal.get_user_by_email.assert_called_once_with("john@example.com")
    mock_dal.create_user.assert_called_once()

@pytest.mark.asyncio
async def test_create_user_duplicate_email():
    """Test validation with mocked dependencies"""
    
    # Arrange: Mock existing user
    mock_dal = Mock(spec=UserDAL)
    mock_dal.get_user_by_email = AsyncMock(
        return_value=UserModel(id=1, name="Existing", email="john@example.com")
    )
    
    service = UserService(dal=mock_dal)
    request = UserRequest(name="John", email="john@example.com")
    
    # Act & Assert: Should raise ValueError
    with pytest.raises(ValueError, match="Email already exists"):
        await service.create_user(request)
```

---

## Author Profile

### VISHNU KIRAN M

**Role**: Senior Software Engineer | AI/ML Specialist  
**Project**: MARVISH Industrial AI Assistant (VishAgent)  
**Location**: Hyderabad, India

#### Expertise
- **Backend Development**: FastAPI, Python, RESTful APIs
- **AI/ML Integration**: OpenAI, LangChain, LangGraph
- **Architecture**: 3-Layer Architecture, Dependency Injection, SOLID Principles
- **Databases**: PostgreSQL, MongoDB
- **Tools**: Docker, Git, VS Code

#### Current Project Focus
- Building AI-powered claim policy analysis system
- Implementing LLM-based tool calling with LangGraph
- Designing clean architecture with proper separation of concerns
- Creating reusable patterns and documentation

#### Technical Philosophy
- **Clean Code**: Emphasize readability and maintainability
- **SOLID Principles**: Apply industry best practices
- **Dependency Injection**: Promote testability and flexibility
- **Documentation**: Comprehensive guides for team and future reference

#### Contact
- **Name**: Vishnu Kiran M
- **Alias**: ViKi Pedia
- **Expertise**: Designing AI Solutions
- **Project Repository**: VishAgent
- **Documentation Style**: Practical, example-driven, detailed
- **Coding Standards**: Type hints, docstrings, proper error handling

#### VishAgent Project Goals
1. Build scalable FastAPI-based AI assistant
2. Implement clean 3-layer architecture (API → Service → DAL)
3. Integrate LangChain and LangGraph for complex workflows
4. Create comprehensive documentation and code snippets
5. Establish patterns for team consistency

---

## Summary: Dependency Injection Quick Reference

| Method | Syntax | Use When | Pros | Cons |
|--------|--------|----------|------|------|
| **Constructor** | `__init__(self, dep)` | Required deps | Explicit, immutable | More boilerplate |
| **FastAPI Depends** | `Depends(get_dep)` | FastAPI endpoints | Automatic, clean | FastAPI-specific |
| **Property** | `@property` setter | Optional deps | Flexible | Invalid state risk |
| **Method** | Method parameter | Per-method deps | Flexible | Cluttered signatures |
| **Interface** | ABC injection | Multiple impls | Very flexible | More complexity |
| **Container** | DI framework | Large apps | Centralized | Learning curve |

---

## Related Files

- [api/api_mange_user/api_user.py](api/api_mange_user/api_user.py) - User endpoints with DI
- [services/user_service.py](services/user_service.py) - Service layer with constructor injection
- [repositories/user_dal.py](repositories/user_dal.py) - DAL layer
- [core/config.py](core/config.py) - Application configuration
- [READMEProjectStructure.md](READMEProjectStructure.md) - Full project structure
