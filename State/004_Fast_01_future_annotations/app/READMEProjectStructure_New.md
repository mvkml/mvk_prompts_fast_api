# VishAgent Project Structure

## Overview

VishAgent is a FastAPI-based AI agent system for claim policy analysis and LLM tool calling. The project follows a **3-layer architecture pattern** (API → Services → DAL) for clean separation of concerns and maintainability.

## Current Project Structure

```
VishAgent/
│
├── app/                                    # Main application package
│   ├── __init__.py
│   ├── main.py                            # FastAPI application entry point
│   ├── requirements.txt                   # Python dependencies
│   ├── README.md                          # Main documentation
│   ├── READMEProjectStructure.md          # This file
│   │
│   ├── api/                               # API Layer (Endpoints/Controllers)
│   │   ├── __init__.py
│   │   ├── router.py                      # Main API router aggregator
│   │   │
│   │   ├── api_pt/                        # Portuguese API endpoints
│   │   │   ├── __init__.py
│   │   │   ├── api_pt.py                  # Basic OpenAI integration
│   │   │   ├── api_lc_pt.py               # LangChain Portuguese
│   │   │   ├── api_lc_pt_01_ft.py         # LangChain Feature 1
│   │   │   ├── api_lc_pt_02_fe.py         # LangChain Feature 2
│   │   │   ├── api_lc_pt_03_ff.py         # LangChain Feature 3
│   │   │   └── api_lc_pt_04_ff.py         # LangChain Feature 4
│   │   │
│   │   ├── api_cpt/                       # Claim Policy Type endpoints
│   │   │   ├── __init__.py
│   │   │   ├── api_lc_cpt_01_ft.py        # Feature 1
│   │   │   ├── api_lc_cpt_02_fm.py        # Feature 2
│   │   │   └── api_lc_cpt_02_sthm.py      # Feature 3
│   │   │
│   │   ├── api_fspt/                      # Full Stack Portuguese Type
│   │   │   ├── __init__.py
│   │   │   ├── api_lc_fspt_01_ft.py       # Feature 1
│   │   │   ├── api_lc_fspt_02_fcpt.py     # Feature 2
│   │   │   └── api_lc_fspt_02_fcpt_mp.py  # Feature 2 (MP version)
│   │   │
│   │   ├── api_mange_user/                # User Management API
│   │   │   ├── __init__.py
│   │   │   ├── api_user.py                # User endpoints (GET, POST, PUT, DELETE, PATCH)
│   │   │   └── router_user.py             # User router aggregator
│   │   │
│   │   └── __pycache__/                   # Python cache
│   │
│   ├── services/                          # Service Layer (Business Logic)
│   │   ├── __init__.py
│   │   ├── user_service.py                # User business logic
│   │   ├── claim_policy_service.py        # Claim policy business logic
│   │   └── llm_service.py                 # LLM integration service
│   │
│   ├── repositories/                      # DAL Layer (Data Access Layer)
│   │   ├── __init__.py
│   │   ├── user_dal.py                    # User data access
│   │   ├── claim_policy_dal.py            # Claim policy data access
│   │   └── base_dal.py                    # Base DAL class (optional)
│   │
│   ├── models/                            # Pydantic Models (DTOs)
│   │   ├── __init__.py
│   │   ├── user_model.py                  # User models (UserRequest, UserResponse)
│   │   ├── claim_model.py                 # Claim models
│   │   ├── prompt_model.py                # Prompt-related models
│   │   │
│   │   ├── common/                        # Shared models
│   │   │   ├── __init__.py
│   │   │   └── common_base.py             # Base model classes
│   │   │
│   │   └── __pycache__/
│   │
│   ├── core/                              # Application Configuration
│   │   ├── __init__.py
│   │   ├── config.py                      # Environment config, settings
│   │   ├── security.py                    # Authentication, authorization
│   │   └── database.py                    # Database connection (planned)
│   │
│   ├── files/                             # Static files and prompts
│   │   └── prompts/                       # Prompt templates
│   │       ├── claim_prompt.txt           # Claim processing prompt
│   │       ├── prasanna_chandra.txt       # Sample data
│   │       └── sravan_vegetable.txt       # Sample data
│   │
│   ├── utils/                             # Utility functions
│   │   ├── __init__.py
│   │   ├── helpers.py                     # General helper functions
│   │   ├── validators.py                  # Custom validators (planned)
│   │   └── constants.py                   # Application constants (planned)
│   │
│   └── __pycache__/
│
├── Documents/                             # Project Documentation
│   ├── 001_Start.txt                      # Getting started guide
│   ├── 002_Work.txt                       # Work instructions
│   ├── 003_Templates.txt                  # Code templates
│   ├── api_lc_fspt_02_fcpt_mp.txt         # Feature documentation
│   ├── F1.txt                             # Feature notes
│   │
│   ├── ClaimPolicy/                       # Claim policy related docs
│   │   ├── ClaimPolicy.txt                # Claim policy patterns
│   │   ├── Weather.txt                    # Weather API docs
│   │   │
│   │   ├── Lan_Graph/                     # LangGraph documentation
│   │   │   └── lan_graph_caluclator.txt   # LangGraph calculator pattern
│   │   │
│   │   └── WeatherAgent/                  # Weather agent docs
│   │       ├── Chat_Completion_Response.txt
│   │       └── Weather.txt
│   │
│   ├── Errors/                            # Error documentation
│   │   └── 001_Error.txt                  # Error tracking
│   │
│   ├── Snippets/                          # Code snippets
│   │   ├── Snippets.md                    # Snippet documentation
│   │   ├── key_bindnig.json               # VS Code key bindings
│   │   └── type_except.json               # Type hints & exceptions
│   │
│   └── Visio/                             # Architecture diagrams
│       ├── OpenAI - Copy.drawio           # OpenAI flow diagram
│       └── OpenAI.drawio                  # OpenAI architecture
│
├── tests/                                 # Unit & Integration Tests
│   ├── __init__.py
│   ├── unit/                              # Unit tests (planned)
│   │   ├── test_user_service.py
│   │   └── test_user_dal.py
│   │
│   ├── integration/                       # Integration tests (planned)
│   │   ├── test_user_endpoints.py
│   │   └── test_api_integration.py
│   │
│   └── fixtures/                          # Test data (planned)
│       └── user_fixtures.py
│
├── .env                                   # Environment variables (not in repo)
├── .env.example                           # Environment template
├── .gitignore                             # Git ignore rules
├── Dockerfile                             # Docker containerization
├── docker-compose.yml                     # Docker orchestration (planned)
├── requirements.txt                       # Python dependencies
└── README.md                              # Root documentation
```

---

## Architecture Layers

### 1. API Layer (api/)
**Responsibility**: HTTP request handling, input validation, response formatting

**Key Components**:
- Route handlers (endpoints)
- Request/response models validation
- HTTP method routing (GET, POST, PUT, DELETE, PATCH)

**Example**:
```python
# api/api_mange_user/api_user.py
@user_router.post("/")
async def create_user(request: UserRequest) -> UserResponse:
    dal = UserDAL()
    service = UserService(dal)
    user = await service.create_user(request)
    response.Data = user
    return response
```

**Files**:
- `api_pt/` - Portuguese API endpoints
- `api_cpt/` - Claim Policy Type endpoints
- `api_fspt/` - Full Stack Portuguese endpoints
- `api_mange_user/` - User management endpoints

---

### 2. Service Layer (services/)
**Responsibility**: Business logic, validation, orchestration

**Key Components**:
- Business rule enforcement
- Service-to-service calls
- Transaction management
- LLM integration

**Example**:
```python
# services/user_service.py
class UserService:
    async def create_user(self, request: UserRequest) -> User:
        # Validation
        if await self.dal.get_user_by_email(request.email):
            raise ValueError("Email already exists")
        
        # Business logic
        user = await self.dal.create_user(request)
        # Additional processing (notifications, logging, etc.)
        return user
```

**Files**:
- `user_service.py` - User operations
- `claim_policy_service.py` - Claim processing
- `llm_service.py` - LLM integration

---

### 3. DAL Layer (repositories/)
**Responsibility**: Database access, CRUD operations, data persistence

**Key Components**:
- Database queries
- ORM/driver interactions
- Connection management
- Query optimization

**Example**:
```python
# repositories/user_dal.py
class UserDAL:
    async def create_user(self, user_request: UserRequest) -> User:
        query = "INSERT INTO users (...) VALUES (...)"
        result = await self.db.fetch_one(query, (...))
        return User(**result)
    
    async def get_user_by_id(self, user_id: int) -> Optional[User]:
        query = "SELECT * FROM users WHERE id = %s"
        result = await self.db.fetch_one(query, (user_id,))
        return User(**result) if result else None
```

**Files**:
- `user_dal.py` - User data operations
- `claim_policy_dal.py` - Claim data operations
- `base_dal.py` - Common DAL functionality

---

## Supporting Layers

### Models Layer (models/)
**Pydantic models** for request/response validation and serialization

```python
# models/user_model.py
class UserRequest(BaseModel):
    name: str
    email: str
    phone: Optional[str]

class UserResponse(BaseModel):
    IsInvalid: bool = False
    Message: Optional[str | dict] = None
    Data: Optional[UserModel] = None
```

### Core Layer (core/)
**Application configuration** and settings

```python
# core/config.py
class Settings:
    app_name: str = "MARVISH Industrial AI Assistant"
    open_ai_key: str
    open_ai_model_name: str = "gpt-4o-mini"
    db_host: str
    db_port: int
    log_level: str = "INFO"
```

### Utils Layer (utils/)
**Reusable utility functions**

- Helper functions
- Validators
- Constants
- Formatters

---

## Data Flow Example: Create User

```
1. HTTP Request
   POST /api/users
   Body: { "name": "John", "email": "john@example.com" }
         ↓
2. API Layer (api_user.py)
   create_user(request: UserRequest) → validate input
         ↓
3. Service Layer (user_service.py)
   UserService.create_user() → business logic, validation
         ↓
4. DAL Layer (user_dal.py)
   UserDAL.create_user() → INSERT INTO users
         ↓
5. Database
   User record created
         ↓
6. Response Chain
   DAL → User object
   Service → User object
   API → UserResponse(Data=User, IsInvalid=False)
         ↓
7. HTTP Response
   200 OK
   {
     "IsInvalid": false,
     "Message": "User created successfully",
     "Data": {...}
   }
```

---

## File Organization Best Practices

### API Layer Organization
```
api/
├── router.py              # Main aggregator
└── {feature}_name/        # Feature module
    ├── __init__.py
    ├── {feature}.py       # Main endpoint file
    ├── router_{name}.py   # Router (optional)
    └── ...
```

### Service Organization
```
services/
├── __init__.py
├── {entity}_service.py    # Service file
└── {feature}_service.py   # Feature service
```

### DAL Organization
```
repositories/
├── __init__.py
├── {entity}_dal.py        # DAL file (also called repository)
└── base_dal.py            # Common functionality
```

### Models Organization
```
models/
├── __init__.py
├── {entity}_model.py      # Entity models
└── common/
    └── common_base.py     # Base models
```

---

## File Naming Conventions

| Layer | Pattern | Example |
|-------|---------|---------|
| API | `api_{name}.py` or `routes_{name}.py` | `api_user.py`, `routes_claims.py` |
| Service | `{entity}_service.py` | `user_service.py` |
| DAL | `{entity}_dal.py` | `user_dal.py` |
| Models | `{entity}_model.py` | `user_model.py` |
| Utils | `{utility}_helper.py` or `{utility}_utils.py` | `email_helper.py` |

---

## Technology Stack

| Component | Technology | Version |
|-----------|-----------|---------|
| Web Framework | FastAPI | 0.111.0 |
| ASGI Server | Uvicorn | 0.30.1 |
| Data Models | Pydantic | Latest |
| LLM Integration | LangChain | 0.3.27 |
| LLM Provider | OpenAI | gpt-4o-mini |
| Graph Framework | LangGraph | 0.4.x |
| Language | Python | 3.9+ |

---

## Current Status

### ✅ Implemented
- [x] FastAPI entry point (main.py)
- [x] API layer structure
- [x] Core configuration
- [x] Multiple endpoint modules
- [x] User API endpoints (fully implemented)
- [x] Models and DTOs
- [x] Documentation (README.md)

### 🔄 In Progress
- [ ] Service layer implementation
- [ ] DAL layer implementation
- [ ] Database integration
- [ ] LangGraph workflows

### 📋 Planned
- [ ] Unit tests
- [ ] Integration tests
- [ ] Authentication/Authorization
- [ ] API rate limiting
- [ ] Logging system
- [ ] Error tracking
- [ ] Docker containerization

---

## Quick Reference

### Running the Application

```bash
# 1. Setup virtual environment
cd C:\v\v\learn\lv_python\ai\VishAgent\app
python -m venv venv
venv\Scripts\activate.bat

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run server (port 825)
python main.py

# 4. Access API
# Swagger: http://127.0.0.1:825/docs
# ReDoc: http://127.0.0.1:825/redoc
```

### Adding a New Endpoint

```python
# 1. Create router in api/{feature}/
# 2. Define endpoint function
@router.post("/{path}")
async def endpoint_name(request: RequestModel) -> ResponseModel:
    response = ResponseModel()
    try:
        # Business logic via service
        dal = EntityDAL()
        service = EntityService(dal)
        result = await service.operation(request)
        response.Data = result
    except Exception as ex:
        response.IsInvalid = True
        response.Message = {"error": str(ex)}
    return response

# 3. Include router in api/router.py
api_router.include_router(entity_router, prefix="/entity")

# 4. Test endpoint
curl -X POST http://localhost:825/api/entity
```

### Adding a New Entity

```
1. Create Model
   models/{entity}_model.py
   - Define {Entity}Request, {Entity}Response, {Entity}Model

2. Create API
   api/{feature}/{entity}.py
   - Define endpoints (GET, POST, PUT, DELETE, PATCH)

3. Create Service
   services/{entity}_service.py
   - Define {Entity}Service with business logic

4. Create DAL
   repositories/{entity}_dal.py
   - Define {Entity}DAL with CRUD operations

5. Register Routes
   api/router.py
   - Include router from api/{feature}/{entity}.py
```

---

## Related Documentation

- [README.md](README.md) - Main project documentation with patterns
- [Snippets.md](../Documents/Snippets/Snippets.md) - Code snippets and templates
- [001_Start.txt](../Documents/001_Start.txt) - Getting started guide
- [ClaimPolicy.txt](../Documents/ClaimPolicy/ClaimPolicy.txt) - Claim processing patterns
