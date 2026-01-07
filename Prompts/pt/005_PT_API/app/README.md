# VishAgent - LangChain PromptTemplate Guide

## Author
**Vishnu Kiran M**

---

## Overview
This guide demonstrates how to use **LangChain PromptTemplate** for building dynamic, reusable prompts with OpenAI language models. The project focuses on the `from_template()` method for creating structured prompts in FastAPI applications.

---

## What is PromptTemplate?

**PromptTemplate** is a LangChain class that creates dynamic, parameterized prompts for language models. Instead of manually formatting strings, PromptTemplate provides a structured way to:

- **Define reusable prompt structures** with placeholder variables
- **Inject dynamic content** safely into prompts
- **Maintain consistency** across multiple API calls
- **Separate prompt logic** from business logic
- **Enable version control** of prompt templates

**Why use PromptTemplate?**
- Eliminates manual string concatenation and formatting errors
- Provides type-safe variable substitution
- Makes prompts testable and maintainable
- Integrates seamlessly with LangChain chains and agents
- Supports complex prompt composition

---

## PromptTemplate Methods

LangChain provides several ways to create PromptTemplate instances:

### 1. **`from_template()` Method** ⭐ (Recommended)
Creates a template from a simple string with `{variable}` placeholders. Most common and easiest approach.

```python
from langchain.prompts import PromptTemplate

template = PromptTemplate.from_template(
    "You are a {role}. Answer this question: {question}"
)
```

### 2. **Constructor Method**
Explicitly defines input variables and template string.

```python
template = PromptTemplate(
    input_variables=["role", "question"],
    template="You are a {role}. Answer this question: {question}"
)
```

### 3. **`from_file()` Method**
Loads templates from external files (txt, json, yaml).

```python
template = PromptTemplate.from_file("prompts/medical_assistant.txt")
```

### 4. **`ChatPromptTemplate`**
For multi-message conversations with system/user/assistant roles.

```python
from langchain.prompts import ChatPromptTemplate

template = ChatPromptTemplate.from_messages([
    ("system", "You are a {role}"),
    ("user", "{question}")
])
```

**This guide focuses on `from_template()` method.**

---

## Deep Dive: `from_template()` Method

### What is `from_template()`?

The `from_template()` method is the **most straightforward way** to create a PromptTemplate in LangChain. It:
- Automatically detects variables enclosed in curly braces `{variable_name}`
- Infers input variables without explicit declaration
- Returns a ready-to-use PromptTemplate instance
- Supports Python f-string-like syntax

### Syntax

```python
from langchain.prompts import PromptTemplate

template = PromptTemplate.from_template(
    template_string,
    template_format="f-string",  # or "jinja2"
    partial_variables=None
)
```

**Parameters:**
- `template` (str): Template string with `{variable}` placeholders
- `template_format` (str, optional): Format type - `"f-string"` (default) or `"jinja2"`
- `partial_variables` (dict, optional): Pre-filled variables

### Basic Example

```python
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

# Create template
template = PromptTemplate.from_template(
    "You are a {role}. Answer this {question} about {topic}."
)

# Format the prompt
prompt = template.format(
    role="medical expert",
    question="What are the benefits",
    topic="health insurance"
)

# Use with ChatOpenAI
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.3)
response = llm.invoke(prompt)
print(response.content)
```

### Advanced Example: Medical Assistant

```python
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

# Complex template with multiple variables
template = PromptTemplate.from_template("""
You are an expert {specialty} assistant with {experience} years of experience.

Patient Context:
- Age: {age}
- Condition: {condition}

Question: {question}

Provide a professional response in {max_words} words or less.
Include {tone} language suitable for patients.
""")

# Format with real data
formatted_prompt = template.format(
    specialty="medical insurance",
    experience=10,
    age=45,
    condition="pre-existing diabetes",
    question="What coverage options are available?",
    max_words=100,
    tone="simple and empathetic"
)

# Invoke LLM
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.3, api_key="your-key")
response = llm.invoke(formatted_prompt)
print(response.content)
```

### Using with LangChain Chains (LCEL)

```python
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

template = PromptTemplate.from_template(
    "Translate '{text}' from {source_lang} to {target_lang}."
)

llm = ChatOpenAI(model="gpt-4o-mini")

# Create chain using LangChain Expression Language
chain = template | llm

# Invoke chain
result = chain.invoke({
    "text": "Good morning",
    "source_lang": "English",
    "target_lang": "Spanish"
})
print(result.content)  # Output: "Buenos días"
```

### Partial Variables

Pre-fill some variables that rarely change:

```python
from langchain.prompts import PromptTemplate
from datetime import datetime

template = PromptTemplate.from_template(
    "Date: {date}\nUser: {user}\nQuestion: {question}",
    partial_variables={"date": datetime.now().strftime("%Y-%m-%d")}
)

# Only need to provide user and question
prompt = template.format(user="John", question="What is a premium?")
print(prompt)
# Output:
# Date: 2026-01-07
# User: John
# Question: What is a premium?
```

---

## Advantages of `from_template()`

### ✅ Pros

1. **Simplicity**: Most intuitive syntax - just write a string with `{variables}`
2. **Auto-detection**: Automatically identifies all variables without manual listing
3. **Less Boilerplate**: No need to specify `input_variables` parameter
4. **Readable**: Template structure is clear and easy to understand
5. **Quick Prototyping**: Fastest way to create prompts during development
6. **Python f-string Familiarity**: Similar to standard Python string formatting
7. **Chain Compatibility**: Works seamlessly with LangChain Expression Language (LCEL)
8. **No Import Overhead**: Same import as regular PromptTemplate
9. **Dynamic Updates**: Easy to modify template strings programmatically
10. **Error Prevention**: Less chance of mismatch between variables and template

### Example: Rapid Development

```python
# Quick iteration - change template without updating input_variables
template_v1 = PromptTemplate.from_template("Answer: {question}")
template_v2 = PromptTemplate.from_template("Context: {context}\nAnswer: {question}")
template_v3 = PromptTemplate.from_template("Role: {role}\nContext: {context}\nAnswer: {question}")
# No need to update input_variables each time!
```

---

## Limitations of `from_template()`

### ❌ Cons

1. **Limited Validation**: No explicit variable declaration means typos might not be caught early
2. **Less Explicit**: Variable requirements are hidden in the template string
3. **Simple Format Only**: Only supports f-string or jinja2 - no custom formatters
4. **Documentation Gap**: Variable names and purposes aren't self-documenting
5. **Type Safety**: No built-in type hints for expected variable types
6. **Complex Logic**: Limited support for conditional logic (use ChatPromptTemplate for complex cases)
7. **Debugging**: Harder to validate template structure before runtime
8. **No IDE Autocomplete**: Variables aren't explicitly listed, so no autocomplete help

### Example: Hidden Variable Risk

```python
# Typo in variable name - only fails at runtime
template = PromptTemplate.from_template(
    "Hello {usre_name}, your {role} is confirmed."  # Typo: usre_name
)

# This will raise KeyError at format time, not template creation time
prompt = template.format(user_name="John", role="admin")  # KeyError!
```

### When NOT to Use `from_template()`

Use the **constructor method** instead when:
- You need explicit documentation of required variables
- Building a library/API where input validation is critical
- Working in a team where variable contracts must be clear
- Need type hints or validation for template variables

```python
# More explicit for production code
template = PromptTemplate(
    input_variables=["user_name", "role"],  # Explicit contract
    template="Hello {user_name}, your {role} is confirmed."
)
```

---

## Tech Stack
- **Framework**: FastAPI 0.111.0
- **Server**: Uvicorn 0.30.1
- **Runtime**: Python 3.10+
- **LLM Integration**:
  - **LangChain** 0.3.27
  - **LangChain-OpenAI** 0.3.35
  - **LangChain-Core** >=0.3.78, <1.0.0
  - **OpenAI Python SDK** (for direct API access)
- **Data Validation**: Pydantic

---

## Installation

### Step 1: Install Core Dependencies
```bash
# Install FastAPI
pip install fastapi==0.111.0
pip install uvicorn[standard]==0.30.1

# Install LangChain ecosystem
pip install langchain==0.3.27
pip install langchain-openai==0.3.35
pip install "langchain-core>=0.3.78,<1.0.0"

# Install OpenAI SDK
pip install openai

# Install environment management
pip install python-dotenv
pip install pydantic-settings
```

### Step 2: Install All Dependencies (Recommended)
```bash
cd C:\v\v\learn\lv_python\ai\VishAgent\app
pip install -r requirements.txt
```

### Critical Version Constraints
```
langchain-core>=0.3.78,<1.0.0  # Must NOT be 1.x
langchain==0.3.27
langchain-openai==0.3.35
```

### Verify Installation
```bash
pip show langchain langchain-core langchain-openai
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

### Step 3: Configure API Key

Create a `.env` file in the `app` directory:

```env
ENV=development
OPEN_AI_KEY=sk-proj-your_actual_openai_key_here
OPEN_AI_MODEL_NAME=gpt-4o-mini
APP_NAME=VishAgent
HOST=127.0.0.1
PORT=825
LOG_LEVEL=INFO
```

**Get Your OpenAI API Key:**
1. Visit [OpenAI Platform](https://platform.openai.com/api-keys)
2. Sign in or create an account
3. Click **Create new secret key**
4. Copy the key (starts with `sk-proj-...`)
5. Paste into `.env` file as `OPEN_AI_KEY=sk-proj-...`

### Step 4: Run the Application
```bash
cd C:\v\v\learn\lv_python\ai\VishAgent\app
python main.py
```

**Access points:**
- API Root: `http://127.0.0.1:825/`
- API Endpoints: `http://127.0.0.1:825/api/api_lc_pt/`

---

## How to Call OpenAI with PromptTemplate

### Method 1: Using ChatOpenAI (Recommended)

```python
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
import os

# Initialize ChatOpenAI
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.3,
    api_key=os.getenv("OPEN_AI_KEY")
)

# Create template
template = PromptTemplate.from_template(
    "You are a {role}. Answer: {question}"
)

# Create chain
chain = template | llm

# Invoke
response = chain.invoke({
    "role": "medical insurance expert",
    "question": "What is a deductible?"
})

print(response.content)
```

### Method 2: Format Then Invoke

```python
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

template = PromptTemplate.from_template(
    "Context: {context}\nQuestion: {question}\nAnswer in {max_words} words."
)

# Format first
formatted_prompt = template.format(
    context="Health insurance basics",
    question="What is copayment?",
    max_words=50
)

# Then invoke
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.3)
response = llm.invoke(formatted_prompt)
print(response.content)
```

### Method 3: Direct OpenAI API (Without LangChain)

```python
from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPEN_AI_KEY"))

# Manual template formatting
role = "medical expert"
question = "What is a premium?"

prompt = f"You are a {role}. Answer this question: {question}"

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": prompt}
    ],
    temperature=0.3
)

print(response.choices[0].message.content)
```

### Method 4: Streaming Responses

```python
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

template = PromptTemplate.from_template("Explain {topic} in simple terms.")
llm = ChatOpenAI(model="gpt-4o-mini", streaming=True)

chain = template | llm

# Stream response
for chunk in chain.stream({"topic": "health insurance deductibles"}):
    print(chunk.content, end="", flush=True)
```

---

## Request & Response Structure

### Understanding ChatOpenAI Response Format

When you invoke ChatOpenAI with a PromptTemplate, the response contains rich metadata about the API call, token usage, and model information.

### Example Request

```python
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

# Create template
template = PromptTemplate.from_template(
    "You are a medical insurance expert. Context: {context}. Question: {question}"
)

# Initialize LLM
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.3)

# Create chain
chain = template | llm

# Invoke with data
response = chain.invoke({
    "context": "Health insurance policy details",
    "question": "What is a deductible?"
})
```

### Example Response Structure

The response object contains multiple layers of information:

```json
{
  "response": {
    "content": "It seems like you're looking to generate a response based on a specific prompt and context. However, you haven't provided the actual prompt or the claim details in the context. Could you please provide those details so I can assist you further?",
    "additional_kwargs": {
      "refusal": null
    },
    "response_metadata": {
      "token_usage": {
        "completion_tokens": 46,
        "prompt_tokens": 57,
        "total_tokens": 103,
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
      },
      "model_provider": "openai",
      "model_name": "gpt-4o-mini-2024-07-18",
      "system_fingerprint": "fp_c4585b5b9c",
      "id": "chatcmpl-CvPdiDMluT2t1P3vbSiIYdqsipWrr",
      "service_tier": "default",
      "finish_reason": "stop",
      "logprobs": null
    },
    "type": "ai",
    "name": null,
    "id": "lc_run--019b990c-72ff-7110-a1a1-1a76638f752e-0",
    "tool_calls": [],
    "invalid_tool_calls": [],
    "usage_metadata": {
      "input_tokens": 57,
      "output_tokens": 46,
      "total_tokens": 103,
      "input_token_details": {
        "audio": 0,
        "cache_read": 0
      },
      "output_token_details": {
        "audio": 0,
        "reasoning": 0
      }
    }
  }
}
```

### Successful Response Example (Domain Answer)

This is an example of a successful LLM response with full metadata. It demonstrates how a well-formed request returns content and usage details you can log or use for cost tracking.

```json
{
    "content": "A UB claim, or Uniform Billing claim, refers to a standardized billing format used by healthcare providers to submit claims for reimbursement to insurance companies. It typically includes details about the services rendered, patient information, and billing codes.",
    "additional_kwargs": {
        "refusal": null
    },
    "response_metadata": {
        "token_usage": {
            "completion_tokens": 44,
            "prompt_tokens": 43,
            "total_tokens": 87,
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
        },
        "model_provider": "openai",
        "model_name": "gpt-4o-mini-2024-07-18",
        "system_fingerprint": "fp_c4585b5b9c",
        "id": "chatcmpl-CvRSynwElmTPLHOaV515tCQozt9zy",
        "service_tier": "default",
        "finish_reason": "stop",
        "logprobs": null
    },
    "type": "ai",
    "name": null,
    "id": "lc_run--019b9977-9596-7f52-af2a-0ad9b2cb6ef1-0",
    "tool_calls": [],
    "invalid_tool_calls": [],
    "usage_metadata": {
        "input_tokens": 43,
        "output_tokens": 44,
        "total_tokens": 87,
        "input_token_details": {
            "audio": 0,
            "cache_read": 0
        },
        "output_token_details": {
            "audio": 0,
            "reasoning": 0
        }
    }
}
```

Use the values in `usage_metadata` and `response_metadata.token_usage` with the cost helper shown below to estimate per-request costs.

### Response Fields Explained

#### Top-Level Fields
- **`content`**: The actual text response from the model
- **`type`**: Message type (`"ai"` for assistant responses)
- **`id`**: LangChain run ID for tracking
- **`tool_calls`**: Array of tool/function calls made by the model
- **`invalid_tool_calls`**: Failed or malformed tool calls

#### Response Metadata
- **`model_name`**: Exact model version used (e.g., `gpt-4o-mini-2024-07-18`)
- **`model_provider`**: API provider (`"openai"`)
- **`system_fingerprint`**: OpenAI system configuration identifier
- **`id`**: OpenAI completion ID (starts with `chatcmpl-`)
- **`finish_reason`**: Why the model stopped (`"stop"`, `"length"`, `"tool_calls"`, etc.)

#### Token Usage
- **`prompt_tokens`**: Input tokens consumed (57 in example)
- **`completion_tokens`**: Output tokens generated (46 in example)
- **`total_tokens`**: Sum of input + output (103 in example)
- **`completion_tokens_details`**: Breakdown of output tokens (reasoning, audio, etc.)
- **`prompt_tokens_details`**: Breakdown of input tokens (cached, audio, etc.)

### Accessing Response Data

```python
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

template = PromptTemplate.from_template("Explain {topic} in simple terms.")
llm = ChatOpenAI(model="gpt-4o-mini")
chain = template | llm

response = chain.invoke({"topic": "health insurance"})

# Access content
print(response.content)

# Access metadata
print(f"Model: {response.response_metadata['model_name']}")
print(f"Total tokens: {response.usage_metadata['total_tokens']}")
print(f"Input tokens: {response.usage_metadata['input_tokens']}")
print(f"Output tokens: {response.usage_metadata['output_tokens']}")
print(f"Finish reason: {response.response_metadata['finish_reason']}")

# Check for tool calls
if response.tool_calls:
    print("Tool calls made:")
    for tool_call in response.tool_calls:
        print(f"  - {tool_call}")
```

### Cost Estimation

Use token counts to estimate API costs:

```python
def estimate_cost(response):
    """
    Estimate OpenAI API cost based on token usage.
    Prices as of January 2026 for gpt-4o-mini:
    - Input: $0.15 per 1M tokens
    - Output: $0.60 per 1M tokens
    """
    input_tokens = response.usage_metadata['input_tokens']
    output_tokens = response.usage_metadata['output_tokens']
    
    input_cost = (input_tokens / 1_000_000) * 0.15
    output_cost = (output_tokens / 1_000_000) * 0.60
    total_cost = input_cost + output_cost
    
    return {
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "total_tokens": input_tokens + output_tokens,
        "input_cost_usd": round(input_cost, 6),
        "output_cost_usd": round(output_cost, 6),
        "total_cost_usd": round(total_cost, 6)
    }

# Usage
response = chain.invoke({"topic": "health insurance"})
cost = estimate_cost(response)
print(f"Total cost: ${cost['total_cost_usd']:.6f}")
```

### Logging Response Data

```python
import json
from datetime import datetime

def log_llm_response(response, request_data):
    """Log LLM requests and responses for monitoring."""
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "request": request_data,
        "response": {
            "content": response.content,
            "model": response.response_metadata.get('model_name'),
            "tokens": {
                "input": response.usage_metadata['input_tokens'],
                "output": response.usage_metadata['output_tokens'],
                "total": response.usage_metadata['total_tokens']
            },
            "finish_reason": response.response_metadata.get('finish_reason'),
            "id": response.id
        }
    }
    
    # Save to file or send to monitoring service
    with open("llm_logs.jsonl", "a") as f:
        f.write(json.dumps(log_entry) + "\n")
    
    return log_entry

# Usage
request_data = {"topic": "health insurance", "max_words": 50}
response = chain.invoke(request_data)
log_llm_response(response, request_data)
```

---

## Exception Handling

### Common Errors and Solutions

#### 1. **Invalid API Key (401 Error)**

**Error:**
```json
{
  "response": {
    "error": "Error code: 401 - {'error': {'message': 'Incorrect API key provided...', 'type': 'invalid_request_error', 'code': 'invalid_api_key'}}"
  }
}
```

**Solution:**
```python
import os
from openai import AuthenticationError
from langchain_openai import ChatOpenAI

try:
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        api_key=os.getenv("OPEN_AI_KEY")
    )
    response = llm.invoke("Test prompt")
except AuthenticationError as e:
    print("❌ Invalid API key. Check your .env file.")
    print(f"Error: {e}")
```

**Checklist:**
- ✅ Verify `.env` file exists in `app/` directory
- ✅ Confirm `OPEN_AI_KEY=sk-proj-...` is correct
- ✅ Restart the application after updating `.env`
- ✅ Get new key from [OpenAI Platform](https://platform.openai.com/api-keys)

#### 2. **Missing Template Variables (KeyError)**

**Error:**
```python
KeyError: 'user_name'
```

**Solution:**
```python
from langchain.prompts import PromptTemplate

template = PromptTemplate.from_template("Hello {user_name}, welcome!")

try:
    prompt = template.format(user_name="John")  # ✅ All variables provided
except KeyError as e:
    print(f"❌ Missing variable: {e}")
    print(f"Required variables: {template.input_variables}")
```

**Best Practice:**
```python
# Validate variables before formatting
template = PromptTemplate.from_template("Hello {user_name}, your role is {role}.")

required_vars = template.input_variables
data = {"user_name": "John"}  # Missing 'role'

missing = set(required_vars) - set(data.keys())
if missing:
    print(f"❌ Missing variables: {missing}")
else:
    prompt = template.format(**data)
```

#### 3. **Rate Limit Error (429)**

**Error:**
```
RateLimitError: Rate limit reached for requests
```

**Solution:**
```python
from openai import RateLimitError
import time

def invoke_with_retry(chain, inputs, max_retries=3):
    for attempt in range(max_retries):
        try:
            return chain.invoke(inputs)
        except RateLimitError as e:
            if attempt < max_retries - 1:
                wait_time = 2 ** attempt  # Exponential backoff
                print(f"⏳ Rate limited. Retrying in {wait_time}s...")
                time.sleep(wait_time)
            else:
                raise e

# Usage
template = PromptTemplate.from_template("Summarize: {text}")
llm = ChatOpenAI(model="gpt-4o-mini")
chain = template | llm

response = invoke_with_retry(chain, {"text": "Your long text here"})
```

#### 4. **Connection Error**

**Error:**
```
ConnectionError: ('Connection aborted.', RemoteDisconnected('Remote end closed connection without response'))
```

**Solution:**
```python
from openai import APIConnectionError
import requests

try:
    llm = ChatOpenAI(model="gpt-4o-mini", timeout=30, max_retries=2)
    response = llm.invoke("Test")
except APIConnectionError as e:
    print("❌ Network error. Check your internet connection.")
    print(f"Error: {e}")
except requests.exceptions.Timeout:
    print("❌ Request timed out. Try again.")
```

#### 5. **Invalid Model Name**

**Error:**
```
InvalidRequestError: model 'gpt-5' does not exist
```

**Solution:**
```python
VALID_MODELS = ["gpt-4o-mini", "gpt-4", "gpt-4-turbo", "gpt-3.5-turbo"]

model_name = "gpt-4o-mini"  # From config

if model_name not in VALID_MODELS:
    print(f"❌ Invalid model: {model_name}")
    print(f"✅ Valid models: {VALID_MODELS}")
else:
    llm = ChatOpenAI(model=model_name)
```

#### 6. **Unexpected Response Format / Placeholder Response**

**Error:**
Sometimes endpoints return placeholder text instead of actual LLM responses, especially during development:

```json
{
  "response": "This endpoint will handle requests related to LangChain Prompt Template API 01 fromtemplate"
}
```

**What it means:**
- Endpoint is not fully implemented
- Route returns placeholder text instead of invoking the LLM
- Template or chain is not properly configured

**Solution:**
```python
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

def validate_response(response):
    """Validate that response is from LLM, not a placeholder."""
    
    # Check if response is a dict with placeholder text
    if isinstance(response, dict) and "response" in response:
        content = response.get("response", "")
        
        # Detect placeholder patterns
        placeholder_keywords = [
            "will handle requests",
            "endpoint will",
            "coming soon",
            "under development",
            "placeholder"
        ]
        
        if any(keyword in content.lower() for keyword in placeholder_keywords):
            raise ValueError(
                f"❌ Received placeholder response instead of LLM output: {content}"
            )
    
    # Check if response is proper LangChain AIMessage
    if hasattr(response, 'content') and hasattr(response, 'response_metadata'):
        if not response.content or len(response.content.strip()) == 0:
            raise ValueError("❌ LLM returned empty response")
        
        return True
    
    return False

# Usage
try:
    template = PromptTemplate.from_template("Explain {topic}")
    llm = ChatOpenAI(model="gpt-4o-mini")
    chain = template | llm
    
    response = chain.invoke({"topic": "health insurance"})
    
    # Validate response
    if validate_response(response):
        print(f"✅ Valid LLM response: {response.content}")
    else:
        print("❌ Invalid response format")
        
except ValueError as e:
    print(f"Validation error: {e}")
```

**Fixing placeholder endpoints:**
```python
# ❌ WRONG: Returning placeholder text
@app.get("/api/prompt")
def get_prompt():
    return {
        "response": "This endpoint will handle requests related to LangChain Prompt Template API 01 fromtemplate"
    }

# ✅ CORRECT: Actually invoking the LLM
@app.get("/api/prompt")
def get_prompt(question: str):
    try:
        template = PromptTemplate.from_template("Answer: {question}")
        llm = ChatOpenAI(model="gpt-4o-mini")
        chain = template | llm
        
        response = chain.invoke({"question": question})
        
        return {
            "response": {
                "content": response.content,
                "model": response.response_metadata.get("model_name"),
                "tokens": response.usage_metadata
            }
        }
    except Exception as e:
        return {"error": str(e)}
```

### Complete Error Handling Example

```python
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from openai import AuthenticationError, RateLimitError, APIConnectionError
import os

def safe_invoke_prompt(role: str, question: str):
    try:
        # Validate API key
        api_key = os.getenv("OPEN_AI_KEY")
        if not api_key or not api_key.startswith("sk-"):
            raise ValueError("❌ Invalid or missing OPEN_AI_KEY in .env")
        
        # Create template
        template = PromptTemplate.from_template(
            "You are a {role}. Answer: {question}"
        )
        
        # Validate variables
        data = {"role": role, "question": question}
        missing = set(template.input_variables) - set(data.keys())
        if missing:
            raise ValueError(f"❌ Missing variables: {missing}")
        
        # Invoke LLM
        llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.3, api_key=api_key)
        chain = template | llm
        response = chain.invoke(data)
        
        return {"success": True, "response": response.content}
    
    except AuthenticationError:
        return {"success": False, "error": "Invalid API key. Check .env file."}
    except RateLimitError:
        return {"success": False, "error": "Rate limit reached. Try again later."}
    except APIConnectionError:
        return {"success": False, "error": "Connection error. Check internet."}
    except KeyError as e:
        return {"success": False, "error": f"Missing variable: {e}"}
    except Exception as e:
        return {"success": False, "error": f"Unexpected error: {str(e)}"}

# Usage
result = safe_invoke_prompt(
    role="medical insurance expert",
    question="What is a deductible?"
)

if result["success"]:
    print(f"✅ Response: {result['response']}")
else:
    print(f"❌ Error: {result['error']}")
```

---

## API Endpoints

### GET `/api/api_lc_pt/format_prompt`

Format a prompt using PromptTemplate.

**Query Parameters:**
- `question` (required): User's question
- `context` (optional): Additional context
- `max_words` (optional, default: 50): Max response length

**Example:**
```bash
curl "http://127.0.0.1:825/api/api_lc_pt/format_prompt?question=What%20is%20a%20deductible&max_words=50"
```

**Response:**
```json
{
  "prompt": "You are an expert medical insurance assistant.\n\nUser Question:\nWhat is a deductible\n\nRelevant Context:\n\n\nAnswer clearly and professionally.\nNote: Provide response in max 50 words only"
}
```

---

## References

### Official Documentation
- [LangChain PromptTemplate Guide](https://python.langchain.com/docs/modules/model_io/prompts/prompt_templates/)
- [LangChain from_template API](https://api.python.langchain.com/en/latest/prompts/langchain_core.prompts.prompt.PromptTemplate.html#langchain_core.prompts.prompt.PromptTemplate.from_template)
- [ChatOpenAI Documentation](https://python.langchain.com/docs/integrations/chat/openai)
- [OpenAI API Reference](https://platform.openai.com/docs/api-reference)
- [LangChain Expression Language (LCEL)](https://python.langchain.com/docs/expression_language/)

### Tutorials & Examples
- [LangChain Quickstart](https://python.langchain.com/docs/get_started/quickstart)
- [OpenAI Function Calling](https://platform.openai.com/docs/guides/function-calling)
- [Prompt Engineering Guide](https://www.promptingguide.ai/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)

### Best Practices
- [LangChain Best Practices](https://python.langchain.com/docs/guides/)
- [OpenAI Best Practices](https://platform.openai.com/docs/guides/production-best-practices)
- [Prompt Engineering Techniques](https://help.openai.com/en/articles/6654000-best-practices-for-prompt-engineering-with-openai-api)

### Related Projects
- [LangChain GitHub](https://github.com/langchain-ai/langchain)
- [OpenAI Python SDK](https://github.com/openai/openai-python)
- [FastAPI GitHub](https://github.com/tiangolo/fastapi)

### Community Resources
- [LangChain Discord](https://discord.gg/langchain)
- [OpenAI Community Forum](https://community.openai.com/)
- [LangChain Twitter](https://twitter.com/langchainai)

---

## Project Structure
```
VishAgent/
├── app/
│   ├── main.py                      # FastAPI entry point
│   ├── api/
│   │   ├── router.py                # Main router
│   │   └── api_pt/
│   │       ├── api_pt.py            # OpenAI direct API
│   │       └── api_lc_pt.py         # PromptTemplate endpoints
│   ├── core/
│   │   └── config.py                # Settings & env config
│   ├── models/                      # Pydantic DTOs
│   └── services/                    # Business logic
├── requirements.txt
├── .env                             # API keys (local only)
└── README.md
```

---

## License
Proprietary - VishAgent

**Author:** Vishnu Kiran M  
**Date:** January 2026
