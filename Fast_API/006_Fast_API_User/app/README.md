# VishAgent - API Endpoint Patterns

## FastAPI Endpoint Pattern

### Standard Endpoint Structure

```python
@user_router.post("/item")
async def get_user(request: UserRequest) -> UserResponse:
    response = UserResponse()
    try:
        return response
    except Exception as ex:
        response.IsInvalid = True
        response.Message = {"error": str(ex)}
        return response
```

### Explanation

#### 1. **Route Decorator**
```python
@user_router.post("/item")
```
- `@user_router.post`: Registers the endpoint as a POST operation on the router
- `"/item"`: URL path for the endpoint (e.g., `/api/item`)
- Alternative HTTP methods: `@router.get()`, `@router.put()`, `@router.delete()`

#### 2. **Async Function Definition**
```python
async def get_user(request: UserRequest) -> UserResponse:
```
- `async def`: Declares an asynchronous function for non-blocking operations
- `get_user`: Function name (note: should ideally match the operation, like `create_item`)
- `request: UserRequest`: Type-annotated request parameter (Pydantic model)
- `-> UserResponse`: Return type annotation for better IDE support and documentation

#### 3. **Response Initialization**
```python
response = UserResponse()
```
- Creates an instance of the response Pydantic model
- Ensures consistent response structure
- Pre-initializes all fields with default values

#### 4. **Try-Except Block**
```python
try:
    return response
except Exception as ex:
    response.IsInvalid = True
    response.Message = {"error": str(ex)}
    return response
```
- **try block**: Contains main business logic
- **except block**: Catches any exceptions during execution
- **Error Handling**:
  - `response.IsInvalid = True`: Sets error flag in response
  - `response.Message = {"error": str(ex)}`: Captures error details
  - Returns response object instead of raising exception (user-friendly pattern)

### Best Practices Applied

| Pattern | Purpose |
|---------|---------|
| **Type Annotations** | Automatic request validation, API documentation generation |
| **Pydantic Models** | Request/response validation, serialization, OpenAPI schema |
| **Try-Except** | Graceful error handling without crashing the endpoint |
| **Structured Response** | Consistent response format with error indicators |
| **Async/Await** | Non-blocking I/O for better performance under load |

### Common Response Model Pattern

```python
from pydantic import BaseModel
from typing import Optional, Any

class UserRequest(BaseModel):
    user_id: int
    name: Optional[str] = None

class UserResponse(BaseModel):
    IsInvalid: bool = False
    Message: Optional[dict | str] = None
    Data: Optional[Any] = None
```

### Enhanced Endpoint Pattern

```python
from fastapi import HTTPException, status

@user_router.post("/item", response_model=UserResponse)
async def create_user_item(request: UserRequest) -> UserResponse:
    """
    Create a new user item.
    
    Args:
        request: UserRequest containing user details
        
    Returns:
        UserResponse with creation status
        
    Raises:
        HTTPException: For critical errors that should return HTTP error codes
    """
    response = UserResponse()
    
    try:
        # Business logic here
        # user_service = UserService()
        # result = await user_service.create_item(request)
        # response.Data = result
        
        response.Message = "Item created successfully"
        return response
        
    except ValueError as ve:
        # Handle validation errors
        response.IsInvalid = True
        response.Message = {"error": f"Validation failed: {str(ve)}"}
        return response
        
    except Exception as ex:
        # Log the error (in production)
        # logger.error(f"Error creating item: {str(ex)}")
        
        response.IsInvalid = True
        response.Message = {"error": "Internal server error", "details": str(ex)}
        return response
```

### Alternative: HTTP Exception Pattern

```python
@user_router.post("/item")
async def get_user(request: UserRequest) -> UserResponse:
    try:
        response = UserResponse()
        # Business logic
        return response
    except ValueError as ve:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(ve)
        )
    except Exception as ex:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )
```

### When to Use Each Pattern

#### Use Structured Response Pattern (Original) When:
- Building consistent API responses across all endpoints
- Client needs to check `IsInvalid` field programmatically
- All responses should return HTTP 200 with error details in body
- Building internal/backend-to-backend APIs

#### Use HTTPException Pattern When:
- Following REST standards strictly
- Client expects standard HTTP status codes (400, 401, 404, 500)
- Building public APIs for third-party consumption
- Need automatic HTTP status code documentation in OpenAPI

### Integration with VishAgent Patterns

```python
@api_pt_router.post("/claim")
async def process_claim(request: ClaimPolicyRequest) -> ClaimPolicyResponse:
    response = ClaimPolicyResponse()
    
    try:
        # Step 1: Service layer call
        service = ClaimPolicyService()
        model = service.validate_claim(request)
        
        # Step 2: LLM Provider call
        llm_result = LLMClaimPolicyProvider().invoke_llm(model=model)
        
        # Step 3: Format response
        response.Data = llm_result.model_dump_json()
        response.Message = "Claim processed successfully"
        
        return response
        
    except ValidationError as ve:
        response.IsInvalid = True
        response.Message = {"validation_errors": str(ve)}
        return response
        
    except Exception as ex:
        response.IsInvalid = True
        response.Message = {"error": str(ex)}
        return response
```

### Key Takeaways

1. **Always use type annotations**: Enables FastAPI's automatic validation and documentation
2. **Initialize response early**: Ensures response object exists for error handling
3. **Catch specific exceptions first**: Handle `ValueError`, `ValidationError` before generic `Exception`
4. **Return structured responses**: Use `IsInvalid` and `Message` for consistent error communication
5. **Use async for I/O operations**: Database queries, API calls, file operations
6. **Document with docstrings**: Helps generate better API documentation
7. **Keep business logic in services**: Endpoints should be thin wrappers around service calls

## Related Files

- [router.py](api/router.py) - Router aggregation
- [api_pt.py](api/api_pt/api_pt.py) - Example endpoints with OpenAI integration
- [ClaimPolicy.txt](../Documents/ClaimPolicy/ClaimPolicy.txt) - Claim validation flow pattern
