# VishAgent AI Coding Instructions

## Project Overview
FastAPI-based AI agent system for claim policy analysis and LLM tool calling using OpenAI and LangGraph. Project is in active development transitioning from MCPBot patterns.

## Architecture & Structure

### Current Implementation
```
app/
├── main.py              # FastAPI entry point (port 825, title: "MARVISH Industrial AI Assistant")
├── api/
│   ├── router.py        # Main router aggregator (minimal setup)
│   └── api_pt/          # API endpoints module
│       └── api_pt.py    # Primary router (incomplete)
├── v1/
│   └── models/          # Pydantic DTOs (empty structure)
└── requirements.txt     # Minimal: fastapi==0.111.0, uvicorn[standard]==0.30.1
```

### Planned Architecture (see [READMEProjectStructure.md](../app/READMEProjectStructure.md))
```
api/v1/routes/ → core/ → services/ → models/ → repositories/ → utils/
```

**Current State**: Basic FastAPI skeleton implemented. Documentation-driven development with patterns from MCPBot project (claim validations, LLM services). Most layered architecture awaits implementation.

## Critical Developer Workflows

### Environment Setup (Windows-specific)
```bash
# 1. Create venv in app/ directory
cd c:\v\v\learn\lv_python\ai\VishAgent\app
python -m venv venv

# 2. Activate (use full path for reliability)
c:\v\v\learn\lv_python\ai\VishAgent\app\venv\Scripts\activate.bat

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run server
cd c:\v\v\learn\lv_python\ai\VishAgent\app
python main.py
```

### Running the Application
**Two server configurations exist**:
- **Development (main.py)**: `python main.py` → `http://127.0.0.1:825` (MARVISH Industrial AI Assistant)
- **Production (documented)**: Port 802 for Swagger UI at `http://127.0.0.1:802/docs`

**API Access Points** (port 802 configuration from [001_Start.txt](../Documents/001_Start.txt)):
- Swagger UI: `http://127.0.0.1:802/docs`
- ReDoc: `http://127.0.0.1:802/redoc`
- OpenAPI JSON: `http://127.0.0.1:802/openapi.json`

**Note**: [main.py](../app/main.py) currently uses port 825, but documentation references port 802. Verify intended configuration before deployment.

## Project-Specific Patterns

### LLM Tool Calling Pattern (from [004_Learn.txt](../Documents/004_Learn.txt))
The project uses OpenAI's function calling with a specific flow:
```python
# 1. Initial call with tools
response = client.chat.completions.create(
    model="gpt-4.1-mini",
    messages=[{"role": "user", "content": prompt}],
    tools=tools,
    tool_choice="auto"
)

# 2. Execute tool and format result
tool_result = execute_function(tool_call)
model.Message = json.dumps(tool_result)

# 3. Final call with tool result
final = client.chat.completions.create(
    model=model.model_name,
    messages=[
        {"role": "user", "content": model.prompt},
        llm_msg,  # Original assistant message with tool_calls
        {
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": json.dumps(tool_result)
        }
    ]
)
```

### Claim Policy Service Pattern (from [ClaimPolicy.txt](../Documents/ClaimPolicy/ClaimPolicy.txt))
Flow: `API Validation → Service → LLM Provider → Response`
```
ClaimPolicyValidations (api_claim_policy_validations.py)
  ↓
ClaimPolicyService (claim_policy_svc.py)
  ↓ model = LLMClaimPolicyProvider().invoke_llm(model=model)
LLMClaimPolicyProvider
```

### LangGraph Integration (from [lan_graph_caluclator.txt](../Documents/ClaimPolicy/Lan_Graph/lan_graph_caluclator.txt))
**Critical Dependency Constraint**:
```bash
# Must maintain compatibility:
langchain-core>=0.3.78,<1.0.0  # NOT 1.x!
langchain==0.3.27
langchain-openai==0.3.35
langgraph>=0.4.x
```

**Tool Definition Pattern**:
```python
# ❌ WRONG - Instance method with @tool decorator
@tool
def tool_add(self, x: float, y: float) -> float:
    """Add two numbers."""
    return x + y

# ✅ CORRECT - Static method or standalone function
@staticmethod
@tool
def tool_add(x: float, y: float) -> float:
    """Add two numbers."""
    return x + y
```

**LLM Requirement**:
```python
# ✅ Use ChatOpenAI (has bind_tools method)
from langchain_openai import ChatOpenAI
llm = ChatOpenAI(model="gpt-4.1-mini")

# ❌ Avoid OpenAI completion model (no bind_tools)
from langchain_openai import OpenAI  # Missing bind_tools()
```

### Model Serialization Pattern (from [004_Learn.txt](../Documents/004_Learn.txt))
```python
# Pydantic models use model_dump_json() for serialization
json_str = tool_schema.model_dump_json()
model.Message = llm_response.model_dump_json()
```

## Key Implementation Notes

1. **Port Discrepancy**: [main.py](../app/main.py) runs on port 825, but documentation ([001_Start.txt](../Documents/001_Start.txt)) specifies port 802
2. **Router Aggregation**: [api/router.py](../app/api/router.py) and [api_pt/api_pt.py](../app/api/api_pt/api_pt.py) are minimal stubs awaiting implementation
3. **Windows Path Format**: Use full absolute paths with backslashes for reliability in activation scripts
4. **Related Projects**: References to `MCPBot` suggest shared patterns/services to be migrated

## External Resources
- Work documentation: [Google Drive folder](https://drive.google.com/drive/folders/1M1cJUJCc1G8iBfmwXUbcX8jtQMG-0-m2)
- Architecture diagrams: [Visio files](../Documents/Visio/)

## When Implementing New Features
1. Follow the layered architecture: validations → services → LLM providers
2. Use `model_dump_json()` for Pydantic serialization (not `dict()` or `json()`)
3. For LangGraph tools, always use `@staticmethod` with `@tool` decorator
4. Maintain OpenAI chat completion pattern: initial call → tool execution → final call with results
5. Check [Documents/](../Documents/) folder for feature-specific patterns before implementing
