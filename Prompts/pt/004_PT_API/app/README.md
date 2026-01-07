# MARVISH Industrial AI Assistant (VishAgent)

## Author
**VISHNU KIRAN M**

---

## Description
This repository is an AI agent system designed for claim policy analysis and LLM tool calling using **ChatOpenAI** and LangGraph. It demonstrates enterprise-ready FastAPI patterns, layered architecture, and production-quality LLM integrations using the **LangChain** framework. The foundation bridges proof-of-concept development with scalable, maintainable AI solutions.

---

## About OpenAI & ChatOpenAI

### What is OpenAI?
**OpenAI** is an artificial intelligence research organization that develops advanced AI models. Their most notable products include:
- **GPT (Generative Pre-trained Transformer)** series: GPT-3.5, GPT-4, GPT-4 Turbo
- **DALL-E**: Image generation models
- **Whisper**: Speech recognition models
- **Embeddings**: Text embedding models for semantic search

OpenAI provides APIs that allow developers to integrate these AI capabilities into applications.

### What is ChatOpenAI?
**ChatOpenAI** is a LangChain wrapper class that provides a convenient interface to interact with OpenAI's chat-based language models (like GPT-3.5-turbo and GPT-4). It:
- Simplifies API calls to OpenAI's chat completion endpoints
- Provides built-in support for message history and context
- Integrates seamlessly with LangChain's ecosystem (chains, agents, tools)
- Handles streaming, function calling, and structured outputs
- Manages retries, timeouts, and error handling

### Key Differences: OpenAI vs ChatOpenAI

| Feature | OpenAI (Raw API) | ChatOpenAI (LangChain) |
|---------|------------------|------------------------|
| **Package** | `openai` | `langchain-openai` |
| **Usage** | Direct API calls with `client.chat.completions.create()` | High-level abstraction with `.invoke()` or `.stream()` |
| **Message Format** | Manual dict construction `[{"role": "user", "content": "..."}]` | Automatic conversion from LangChain message objects |
| **Integration** | Standalone, requires custom code for chains | Native LangChain integration with chains, agents, tools |
| **Prompt Templates** | Manual string formatting | Built-in `PromptTemplate` and composition |
| **Streaming** | Manual chunk handling | Built-in streaming with callbacks |
| **Function Calling** | Manual tool schema definition | `.bind_tools()` method with automatic schema generation |
| **Memory/History** | Manual state management | Built-in memory classes (BufferMemory, etc.) |
| **Best For** | Low-level control, custom implementations | Rapid development, complex workflows, agent systems |

**When to use OpenAI directly:**
- You need fine-grained control over API parameters
- Simple, single-shot completions without chains
- Custom retry logic or specialized error handling

**When to use ChatOpenAI:**
- Building conversational agents or chatbots
- Using LangChain tools, chains, or agents
- Need for prompt templates and composition
- Working with memory and conversation history
- Implementing RAG (Retrieval-Augmented Generation) patterns

---

## Project Architecture

This project uses **both** approaches:
1. **Direct OpenAI API** (`app/api/api_pt/api_pt.py`) - For fine-grained control and custom function calling
2. **ChatOpenAI with LangChain** (`app/api/api_pt/api_lc_pt.py`) - For prompt templates and agent workflows

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
- **LLM Integration**:
  - **OpenAI Python SDK** (`openai`) - Direct API access
  - **LangChain** (`langchain`, `langchain-openai`) - High-level abstractions
  - **ChatOpenAI** - LangChain's OpenAI wrapper
  - **PromptTemplate** - LangChain's template system
- **Graph/Agents**: LangGraph (0.4.x) + LangChain 0.3.27
- **Database**: (Configurable via environment)

---

## Prerequisites & Installation

### Step 1: Install Core Dependencies
```bash
# Install FastAPI and OpenAI SDK (direct API access)
pip install fastapi==0.111.0
pip install uvicorn[standard]==0.30.1
pip install openai

# Install LangChain ecosystem (ChatOpenAI + PromptTemplate)
pip install langchain==0.3.27
pip install langchain-openai==0.3.35
pip install "langchain-core>=0.3.78,<1.0.0"

# Install LangGraph for agent workflows
pip install langgraph

# Install Python environment management
pip install python-dotenv
pip install pydantic-settings
```

### Step 2: Install All Dependencies (Recommended)
```bash
cd C:\v\v\learn\lv_python\ai\VishAgent\app
pip install -r requirements.txt
```

### Critical Version Constraints
For LangGraph and LangChain integration to work properly:
```
langchain-core>=0.3.78,<1.0.0  # NOT 1.x (incompatible with langchain 0.3.27)!
langchain==0.3.27
langchain-openai==0.3.35
langgraph>=0.4.x
```

### Verify Installation
```bash
pip show openai langchain langchain-core langchain-openai langgraph
```

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
│   │       ├── api_pt.py            # OpenAI direct API endpoints
│   │       └── api_lc_pt.py         # ChatOpenAI + PromptTemplate endpoints
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

### Step 4: Configure Environment Variables
Create a `.env` file in the `app` directory with the following variables:

```env
ENV=development
OPEN_AI_KEY=your_openai_api_key_here
OPEN_AI_MODEL_NAME=gpt-4o-mini
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

**⚠️ IMPORTANT - OpenAI API Key Setup:**

The OpenAI client requires the API key to be configured. You have two options:

**Option 1: Using `.env` file (Recommended for Development)**
- Create a `.env` file in the `app` directory (same level as `main.py`)
- Add your OpenAI API key: `OPEN_AI_KEY=sk-...`
- The application will automatically load this via `pydantic-settings`

**Option 2: Using System Environment Variable (Recommended for Production)**
```bash
# Windows (PowerShell):
$env:OPENAI_API_KEY="sk-..."

# Windows (Command Prompt):
set OPENAI_API_KEY=sk-...

# Or set permanently in Windows Environment Variables:
# Settings → Environment Variables → New (user variable)
# Variable name: OPENAI_API_KEY
# Variable value: sk-...
```

**Troubleshooting - "api_key client option must be set" Error:**

If you encounter:
```json
{
  "response": {
    "error": "The api_key client option must be set either by passing api_key to the client or by setting the OPENAI_API_KEY environment variable"
  }
}
```

Follow these steps:
1. **Verify `.env` file exists** at `C:\v\v\learn\lv_python\ai\VishAgent\app\.env`
2. **Check API key format**: Should start with `sk-` and be ~48 characters
3. **Verify environment loading**: The code reads `OPEN_AI_KEY` from settings, which must be mapped to the OpenAI client
4. **Restart the application** after adding/changing the `.env` file
5. **Check file permissions**: Ensure the `.env` file is readable by the Python process

**Getting Your OpenAI API Key:**
1. Go to [OpenAI Platform](https://platform.openai.com/api-keys)
2. Sign in with your OpenAI account (create one if needed)
3. Navigate to **API keys** section
4. Click **Create new secret key**
5. Copy the key immediately (it won't be shown again)
6. Paste into your `.env` file as `OPEN_AI_KEY=sk-...`

---

## Running the Application

### Development Mode (Recommended)
```bash
cd C:\v\v\learn\lv_python\ai\VishAgent\app
python main.py
```

**Access points:**
- API Root: `http://127.0.0.1:825/`
- OpenAI Direct API: `http://127.0.0.1:825/api/api_pt/`
- ChatOpenAI/PromptTemplate API: `http://127.0.0.1:825/api/api_lc/`
- Config Endpoint: `http://127.0.0.1:825/api/api_pt/config`

### Production Mode
```bash
python -m uvicorn app.main:app --host 127.0.0.1 --port 802 --reload
```

**API Documentation:**
- Swagger UI: `http://127.0.0.1:802/docs`
- ReDoc: `http://127.0.0.1:802/redoc`
- OpenAPI JSON: `http://127.0.0.1:802/openapi.json`

---

## Sample Usage: ChatOpenAI & PromptTemplate

### 1. Using ChatOpenAI (LangChain Approach)

```python
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain_core.messages import HumanMessage, SystemMessage
import os

# Initialize ChatOpenAI
llm = ChatOpenAI(
    model="gpt-4o-mini",  # or "gpt-4", "gpt-3.5-turbo"
    temperature=0.7,
    api_key=os.getenv("OPEN_AI_KEY")
)

# Simple invocation
response = llm.invoke([
    SystemMessage(content="You are a helpful medical insurance assistant."),
    HumanMessage(content="What is a deductible?")
])
print(response.content)

# With streaming
for chunk in llm.stream("Explain copayment in simple terms"):
    print(chunk.content, end="", flush=True)
```

### 2. Using PromptTemplate

```python
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

# Define a prompt template
template = """
You are an expert medical insurance assistant.

User Question:
{question}

Relevant Context:
{context}

Answer clearly and professionally.
Note: Provide response in max {max_words} words only
"""

prompt = PromptTemplate(
    input_variables=["question", "context", "max_words"],
    template=template
)

# Format the prompt
formatted_prompt = prompt.format(
    question="What is a health insurance premium?",
    context="User is a new policyholder with basic coverage",
    max_words=50
)

# Invoke LLM with formatted prompt
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.3)
response = llm.invoke(formatted_prompt)
print(response.content)
```

### 3. Using Chain with PromptTemplate

```python
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain.chains import LLMChain

# Create template
template = PromptTemplate(
    input_variables=["question", "context"],
    template="Context: {context}\n\nQuestion: {question}\n\nAnswer:"
)

# Create LLM
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.3)

# Create chain (Note: LLMChain is deprecated in favor of LCEL)
# Modern approach using LangChain Expression Language (LCEL):
chain = template | llm

# Invoke chain
result = chain.invoke({
    "question": "What are the benefits of preventive care?",
    "context": "Preventive care includes annual checkups and screenings"
})
print(result.content)
```

### 4. Using ChatOpenAI with Tools (Function Calling)

```python
from langchain_openai import ChatOpenAI
from langchain.tools import tool

# Define a tool
@tool
def get_policy_details(policy_id: str) -> dict:
    """Get policy details by policy ID."""
    return {
        "policy_id": policy_id,
        "coverage": "Comprehensive",
        "deductible": 1000,
        "premium": 250
    }

# Initialize ChatOpenAI with tools
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
llm_with_tools = llm.bind_tools([get_policy_details])

# Invoke with tool binding
response = llm_with_tools.invoke("Get details for policy ID ABC123")
print(response.tool_calls)  # Check if tool was called
```

### 5. Using Direct OpenAI API (For Comparison)

```python
from openai import OpenAI
import os

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPEN_AI_KEY"))

# Make API call
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a helpful medical insurance assistant."},
        {"role": "user", "content": "What is a deductible?"}
    ],
    temperature=0.7
)

print(response.choices[0].message.content)
```

---

## API Endpoints

### OpenAI Direct API Endpoints (`/api/api_pt`)

#### GET `/api/api_pt/`
Returns default response from OpenAI direct API router.

**Response:**
```json
{
  "message": "Default response from api_pt"
}
```

#### GET `/api/api_pt/config`
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

#### GET `/api/api_pt/prompt`
Echo endpoint for testing prompt passing.

**Query Parameters:**
- `prompt` (string): Your prompt text

**Example:**
```bash
curl "http://127.0.0.1:825/api/api_pt/prompt?prompt=test"
```

**Response:**
```json
{
  "prompt": "test"
}
```

### ChatOpenAI + PromptTemplate Endpoints (`/api/api_lc`)

#### GET `/api/api_lc/prompt_template`
Returns the base prompt template with configurable word limit.

**Query Parameters:**
- `max_words` (optional, default: 50): Maximum word count for responses

**Example:**
```bash
curl "http://127.0.0.1:825/api/api_lc/prompt_template?max_words=100"
```

**Response:**
```json
{
  "template": "\nYou are an expert medical insurance assistant.\n\nUser Question:\n{question}\n\nRelevant Context:\n{context}\n\nAnswer clearly and professionally.\nNote: Provide response in max 100 words only\n"
}
```

#### GET `/api/api_lc/format_prompt`
Returns a fully formatted prompt using the template.

**Query Parameters:**
- `question` (required): The user's question
- `context` (optional, default: ""): Additional context
- `max_words` (optional, default: 50): Maximum word count

**Example:**
```bash
curl "http://127.0.0.1:825/api/api_lc/format_prompt?question=What%20is%20a%20deductible&context=Health%20insurance&max_words=50"
```

**Response:**
```json
{
  "prompt": "\nYou are an expert medical insurance assistant.\n\nUser Question:\nWhat is a deductible\n\nRelevant Context:\nHealth insurance\n\nAnswer clearly and professionally.\nNote: Provide response in max 50 words only\n"
}
```

---

## Key Implementation Patterns

### 1. ChatOpenAI with PromptTemplate (LangChain)
```python
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

# Create template
template = PromptTemplate(
    input_variables=["question", "context", "max_words"],
    template="""
You are an expert medical insurance assistant.

User Question:
{question}

Relevant Context:
{context}

Answer clearly and professionally.
Note: Provide response in max {max_words} words only
"""
)

# Initialize ChatOpenAI
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.3)

# Create chain
chain = template | llm

# Invoke
result = chain.invoke({
    "question": "What is copayment?",
    "context": "Health insurance basics",
    "max_words": 50
})
print(result.content)
```

### 2. Direct OpenAI Function Calling
```python
from openai import OpenAI

client = OpenAI(api_key="your-key")

# Initial call with tools
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": prompt}],
    tools=tools,
    tool_choice="auto"
)

# Execute tool and format result
tool_result = execute_function(tool_call)

# Final call with tool result
final = client.chat.completions.create(
    model="gpt-4o-mini",
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

### 3. LangGraph Tool Definition
```python
from langchain.tools import tool

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

**Example API response (masked key):**
```json
{
    "response": {
        "error": "Error code: 401 - {'error': {'message': 'Incorrect API key provided: sk-proj-********************************************************************************************************************************************************5fMA. You can find your API key at https://platform.openai.com/account/api-keys.', 'type': 'invalid_request_error', 'code': 'invalid_api_key', 'param': null}, 'status': 401}"
    }
}
```
This 401 error means the key sent to OpenAI is wrong, expired, or missing.

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
4. Integrate ChatOpenAI for claim analysis
5. Implement LangGraph workflows for agent-based processing
6. Add database integration via repositories
7. Create conversational agents with memory
8. Implement RAG (Retrieval-Augmented Generation) pipelines

---

## Resources
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [OpenAI Python SDK](https://github.com/openai/openai-python)
- [LangChain Documentation](https://python.langchain.com/)
- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [ChatOpenAI Guide](https://python.langchain.com/docs/integrations/chat/openai)
- [PromptTemplate Guide](https://python.langchain.com/docs/modules/model_io/prompts/prompt_templates/)
- [OpenAI Function Calling](https://platform.openai.com/docs/guides/function-calling)
- Project Docs: `Documents/` folder

---

## License
Proprietary - MARVISH Industrial AI Assistant
