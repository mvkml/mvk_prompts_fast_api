# MARVISH Industrial AI Assistant (VishAgent)

## Author
**VISHNU KIRAN M**

---

## Description
This repository is an AI agent system designed for claim policy analysis and LLM tool calling using OpenAI and LangGraph. It demonstrates enterprise-ready FastAPI patterns, layered architecture, and production-quality LLM integrations. The foundation bridges proof-of-concept development with scalable, maintainable AI solutions.

---

## About Project
VishAgent is a FastAPI-based AI service that:
- Processes policy claims using intelligent validation layers
- Integrates OpenAI's function calling for dynamic tool execution
- Leverages LangGraph for stateful agent workflows
- Follows N-tier architecture (validations → services → LLM providers → responses)
- Provides structured API endpoints for claim analysis and AI processing

This project serves as a template for building enterprise AI microservices with proper separation of concerns and scalable patterns.

---

## Tech Stack
- **Framework**: FastAPI 0.111.0
- **Server**: Uvicorn 0.30.1
- **Runtime**: Python 3.10+
- **Data Validation**: Pydantic
- **LLM**: OpenAI ChatGPT-4 Mini
- **Graph**: LangGraph (0.4.x) + LangChain 0.3.27
- **Database**: (Configurable via environment)

---

## Project Structure
```
VishAgent/
├── app/
│   ├── main.py                      # FastAPI entry point (port 825)
│   ├── api/
│   │   ├── router.py                # Main router aggregator
│   │   └── api_pt/
│   │       ├── __init__.py
│   │       └── api_pt.py            # Primary API endpoints
│   ├── core/
│   │   ├── __init__.py
│   │   └── config.py                # Settings & environment configuration
│   ├── models/                      # Pydantic DTOs
│   ├── services/                    # Business logic layer
│   └── utils/                       # Helper functions
├── requirements.txt                 # Python dependencies
├── .env                             # Environment variables (local only)
├── README.md
└── READMEProjectStructure.md        # Planned architecture

```

---

## Environment Setup (Windows)

### Step 1: Create Virtual Environment
```bash
cd C:\v\v\learn\lv_python\ai\VishAgent\app
python -m venv venv
```

### Step 2: Activate Virtual Environment
```bash
C:\v\v\learn\lv_python\ai\VishAgent\app\venv\Scripts\activate.bat
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment
Create `.env` file in the app root directory with required variables:
```env
ENV=development
OPEN_AI_KEY=your_openai_key_here
APP_NAME=MARVISH Industrial AI Assistant
HOST=127.0.0.1
PORT=825
DB_HOST=localhost
DB_PORT=5432
DB_NAME=vishagent
DB_USER=admin
DB_PASSWORD=your_password
LOG_LEVEL=INFO
```

---

## Running the Application

### Development Mode (Recommended)
```bash
cd C:\v\v\learn\lv_python\ai\VishAgent\app
python main.py
```

**Access points:**
- API Root: `http://127.0.0.1:825/`
- Config Endpoint: `http://127.0.0.1:825/api/api_pt/config`
- Prompt Endpoint: `http://127.0.0.1:825/api/api_pt/prompt?prompt=your_prompt_here`

### Production Mode
```bash
python -m uvicorn app.main:app --host 127.0.0.1 --port 802 --reload
```

**API Documentation:**
- Swagger UI: `http://127.0.0.1:802/docs`
- ReDoc: `http://127.0.0.1:802/redoc`
- OpenAPI JSON: `http://127.0.0.1:802/openapi.json`

---

## Current API Endpoints

### GET `/`
Returns API initialization message.

**Response:**
```json
{
  "message": "API initialized"
}
```

### GET `/api/api_pt/`
Returns default response from api_pt router.

**Response:**
```json
{
  "message": "Default response from api_pt"
}
```

### GET `/api/api_pt/config`
Returns current application settings (useful for debugging environment setup).

**Response:**
```json
{
  "env": "development",
  "open_ai_key": "sk-...",
  "app_name": "MARVISH Industrial AI Assistant",
  "host": "127.0.0.1",
  "port": 825,
  "db_host": "localhost",
  "db_port": 5432,
  "db_name": "vishagent",
  "db_user": "admin",
  "db_password": "***",
  "log_level": "INFO"
}
```

### GET `/api/api_pt/prompt`
Echo endpoint for testing prompt passing.

**Query Parameters:**
- `prompt` (string): Your prompt text

**Response:**
```json
{
  "prompt": "your_prompt_here"
}
```

**Sample OpenAI Completion Response:**
```json
{
  "id": "chatcmpl-Cv475ofq8ll3Obge3s26qgUN9hBAR",
  "choices": [
    {
      "finish_reason": "stop",
      "index": 0,
      "logprobs": null,
      "message": {
        "content": "Hyderabad, a major city in India, offers various medical insurance options. Residents can choose from numerous providers, including public and private insurers, to find plans that suit their healthcare needs. It's advisable to compare coverage, premiums, and network hospitals before making a decision.",
        "refusal": null,
        "role": "assistant",
        "annotations": [],
        "audio": null,
        "function_call": null,
        "tool_calls": null
      }
    }
  ],
  "created": 1767716543,
  "model": "gpt-4o-mini-2024-07-18",
  "object": "chat.completion",
  "service_tier": "default",
  "system_fingerprint": "fp_c4585b5b9c",
  "usage": {
    "completion_tokens": 53,
    "prompt_tokens": 62,
    "total_tokens": 115,
    "completion_tokens_details": {
      "accepted_prediction_tokens": 0,
      "audio_tokens": 0,
      "reasoning_tokens": 0,
      "rejected_prediction_tokens": 0
    },
    "prompt_tokens_details": {
      "audio_tokens": 0,
      "cached_tokens": 0
    }
  }
}
```

---

## Key Implementation Patterns

### 1. LLM Tool Calling (OpenAI Function Calling)
```python
# Initial call with tools
response = client.chat.completions.create(
    model="gpt-4-mini",
    messages=[{"role": "user", "content": prompt}],
    tools=tools,
    tool_choice="auto"
)

# Execute tool and format result
tool_result = execute_function(tool_call)

# Final call with tool result
final = client.chat.completions.create(
    model="gpt-4-mini",
    messages=[
        {"role": "user", "content": prompt},
        llm_msg,  # Original assistant message
        {
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": json.dumps(tool_result)
        }
    ]
)
```

### 2. Claim Policy Service Flow
```
API Validations → Service Layer → LLM Provider → Response
```

### 3. LangGraph Tool Definition (Required Pattern)
```python
# ✅ CORRECT: Use static method with @tool decorator
@staticmethod
@tool
def tool_add(x: float, y: float) -> float:
    """Add two numbers."""
    return x + y

# ❌ WRONG: Instance methods don't work with @tool
```

### 4. Pydantic Serialization
```python
# Always use model_dump_json() for serialization
json_str = model.model_dump_json()
```

---

## Dependencies & Versions

### Critical Version Constraints
For LangGraph integration to work properly:
```
langchain-core>=0.3.78,<1.0.0  # NOT 1.x!
langchain==0.3.27
langchain-openai==0.3.35
langgraph>=0.4.x
```

### Install with Constraints
```bash
pip install "langchain-core>=0.3.78,<1.0.0"
pip install langchain==0.3.27
pip install langchain-openai==0.3.35
pip install langgraph
```

### Verify Installation
```bash
pip show langchain langchain-core langchain-openai langgraph
```

---

## Configuration Management

Environment variables are loaded via `app/core/config.py` using Pydantic Settings:
- Development mode: Load from `.env` file
- Production mode: Use system environment variables
- All sensitive data (API keys, passwords) should be stored in `.env` (never commit)

---

## Troubleshooting

### Port Already in Use
If port 825 is already in use, modify `main.py` or run with a different port:
```bash
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

### Import Errors
Ensure you're running commands from the correct directory:
```bash
cd C:\v\v\learn\lv_python\ai\VishAgent\app
```

### LangGraph Issues
Verify correct versions are installed:
```bash
pip show langchain langchain-core langgraph
```

### Invalid OpenAI API Key
If you encounter authentication errors when calling OpenAI APIs, check:

**Symptom:**
```
openai.AuthenticationError: Error code: 401 - {'error': {'message': 'Incorrect API key provided...', 'type': 'invalid_request_error', 'param': None, 'code': 'invalid_api_key'}}
```

**Solution:**
1. Verify your `.env` file contains a valid OpenAI API key:
```env
OPEN_AI_KEY=sk-proj-...your_actual_key_here
```

2. Check that the key is properly loaded:
```bash
# Test config endpoint
curl http://127.0.0.1:825/api/api_pt/config
```

3. Common issues:
   - Key contains extra spaces or quotes
   - Using an expired or revoked key
   - Key doesn't have proper permissions
   - `.env` file is not in the correct directory (`app/` folder)

4. Get a new key from [OpenAI Platform](https://platform.openai.com/api-keys)

5. After updating `.env`, restart the server:
```bash
# Stop server (Ctrl+C)
python main.py  # Restart
```

**Note**: Never commit `.env` file to version control. Add it to `.gitignore`.

---

## Next Steps
1. Implement additional routes in `api/api_pt/api_pt.py`
2. Build service layer in `services/`
3. Add Pydantic models to `models/`
4. Integrate LLM providers for claim analysis
5. Implement LangGraph workflows for agent-based processing
6. Add database integration via repositories

---

## Resources
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [OpenAI Function Calling](https://platform.openai.com/docs/guides/function-calling)
- Project Docs: `Documents/` folder

---

## License VISHNU KIRAN M
Proprietary - MARVISH Industrial AI Assistant
