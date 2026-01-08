# VishAgent - LangChain PromptTemplate.from_examples() Guide

## Author
**Vishnu Kiran M**  
**Expertise in designing AI solutions**

---

## Overview
This guide demonstrates how to use **LangChain FewShotPromptTemplate** (the `from_examples()` approach) for building Few-Shot learning prompts with OpenAI language models. This method enables rapid prompt creation using example-based patterns, making it ideal for teaching models specific response formats through demonstrations.

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
- Supports complex prompt composition and few-shot learning

---

## PromptTemplate Methods

LangChain provides several ways to create PromptTemplate instances:

### 1. **Constructor Method**
Explicitly defines input variables and template string.

```python
from langchain.prompts import PromptTemplate

template = PromptTemplate(
    input_variables=["role", "question"],
    template="You are a {role}. Answer this question: {question}"
)
```

### 2. **`from_template()` Method**
Creates a template from a simple string with `{variable}` placeholders.

```python
template = PromptTemplate.from_template(
    "You are a {role}. Answer this question: {question}"
)
```

### 3. **`from_file()` Method**
Loads templates from external files (txt, json, yaml).

```python
template = PromptTemplate.from_file("prompts/medical_assistant.txt")
```

### 4. **`from_examples()` Method** ⭐ (Focus of this guide)
Creates templates using few-shot learning patterns with example-based demonstrations.

```python
from langchain.prompts import FewShotPromptTemplate, PromptTemplate

# Define examples
examples = [
    {"input": "What is a deductible?", "output": "A deductible is the amount you pay before insurance coverage begins."},
    {"input": "What is a copayment?", "output": "A copayment is a fixed fee you pay for a medical service."}
]

# Create example template
example_template = PromptTemplate(
    input_variables=["input", "output"],
    template="Q: {input}\nA: {output}"
)

# Create few-shot template
few_shot_template = FewShotPromptTemplate(
    examples=examples,
    example_prompt=example_template,
    prefix="You are a medical insurance expert. Here are some examples:",
    suffix="Q: {input}\nA:",
    input_variables=["input"]
)
```

### 5. **`ChatPromptTemplate`**
For multi-message conversations with system/user/assistant roles.

```python
from langchain.prompts import ChatPromptTemplate

template = ChatPromptTemplate.from_messages([
    ("system", "You are a {role}"),
    ("user", "{question}")
])
```

**This guide focuses on the `from_examples()` method for few-shot learning.**

---

## Deep Dive: `from_examples()` Method

### What is `from_examples()`?

The `from_examples()` approach uses **FewShotPromptTemplate**, which is designed for **few-shot learning** - a technique where you teach the model by providing example input-output pairs. This method:

- Demonstrates desired response patterns through examples
- Teaches specific formatting, tone, or structure
- Improves response consistency without fine-tuning
- Reduces prompt engineering trial-and-error
- Works well with complex or domain-specific outputs

### Core Components

1. **Examples**: List of dictionaries with input-output pairs
2. **Example Template**: Defines how each example is formatted
3. **Prefix**: Context or instructions before examples
4. **Suffix**: Final prompt after examples (usually includes the actual question)
5. **Input Variables**: Variables to inject into the final prompt

### Syntax

```python
from langchain.prompts import FewShotPromptTemplate, PromptTemplate

few_shot_template = FewShotPromptTemplate(
    examples=examples,                    # List of example dicts
    example_prompt=example_template,      # PromptTemplate for each example
    prefix="instruction_text",            # Context/instructions
    suffix="final_prompt_with_{variable}",# Final question template
    input_variables=["variable"],         # Variables for suffix
    example_separator="\n\n"              # Separator between examples (optional)
)
```

**Parameters:**
- `examples` (List[dict]): List of example dictionaries
- `example_prompt` (PromptTemplate): Template for formatting each example
- `prefix` (str): Text before examples (instructions/context)
- `suffix` (str): Text after examples (actual query)
- `input_variables` (List[str]): Variables used in suffix
- `example_separator` (str, optional): Separator between examples (default: "\n\n")

**Common pitfall:** `PromptTemplate.from_examples()` expects a list of formatted strings. Passing a list of dictionaries (e.g., `{"question": ..., "answer": ...}`) triggers `sequence item 1: expected str instance, dict found`. Convert dictionaries to strings before calling `from_examples()`:

```python
raw_examples = [
    {"question": "What is UB claim?", "answer": "UB claim refers to Uniform Billing used for hospital claims."},
    {"question": "What is EOB?", "answer": "EOB stands for Explanation of Benefits provided by insurers."}
]

examples = [f"Question: {ex['question']}\nAnswer: {ex['answer']}" for ex in raw_examples]
prompt = PromptTemplate.from_examples(
    examples=examples,
    suffix="Question: {question}\nAnswer:",
    input_variables=["question"]
)
```

### Basic Example: Medical Insurance Assistant

```python
from langchain.prompts import FewShotPromptTemplate, PromptTemplate
from langchain_openai import ChatOpenAI

# Step 1: Define training examples
examples = [
    {
        "input": "What is a deductible?",
        "output": "A deductible is the amount you must pay out-of-pocket for covered healthcare services before your insurance plan starts to pay."
    },
    {
        "input": "What is a copayment?",
        "output": "A copayment (copay) is a fixed amount you pay for a covered healthcare service, usually when you receive the service."
    },
    {
        "input": "What is coinsurance?",
        "output": "Coinsurance is your share of the costs of a covered healthcare service, calculated as a percentage (e.g., 20%) of the allowed amount."
    }
]

# Step 2: Create example formatter
example_template = PromptTemplate(
    input_variables=["input", "output"],
    template="Question: {input}\nAnswer: {output}"
)

# Step 3: Create few-shot template
few_shot_template = FewShotPromptTemplate(
    examples=examples,
    example_prompt=example_template,
    prefix="You are an expert medical insurance assistant. Answer questions clearly and concisely based on these examples:",
    suffix="Question: {input}\nAnswer:",
    input_variables=["input"]
)

# Step 4: Format and use
formatted_prompt = few_shot_template.format(input="What is an out-of-pocket maximum?")
print(formatted_prompt)

# Step 5: Invoke with ChatOpenAI
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.3)
response = llm.invoke(formatted_prompt)
print(response.content)
```

### Advanced Example: Structured JSON Responses

```python
from langchain.prompts import FewShotPromptTemplate, PromptTemplate
from langchain_openai import ChatOpenAI
import json

# Examples with structured JSON output
examples = [
    {
        "input": "UB-04 claim for hospital admission",
        "output": json.dumps({
            "claim_type": "UB-04",
            "service_type": "Inpatient Hospital",
            "form_type": "Institutional",
            "typical_services": ["Room and board", "Surgery", "Lab tests"]
        }, indent=2)
    },
    {
        "input": "CMS-1500 claim for doctor visit",
        "output": json.dumps({
            "claim_type": "CMS-1500",
            "service_type": "Professional Services",
            "form_type": "Professional",
            "typical_services": ["Office visit", "Consultation", "Procedures"]
        }, indent=2)
    }
]

# Example template for JSON
example_template = PromptTemplate(
    input_variables=["input", "output"],
    template="Input: {input}\nOutput:\n{output}"
)

# Few-shot template
few_shot_template = FewShotPromptTemplate(
    examples=examples,
    example_prompt=example_template,
    prefix="You are a medical billing expert. Given a claim description, return structured JSON with claim details. Follow these examples:",
    suffix="Input: {input}\nOutput:",
    input_variables=["input"],
    example_separator="\n\n---\n\n"
)

# Use it
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.2)
formatted_prompt = few_shot_template.format(input="DME claim for wheelchair")
response = llm.invoke(formatted_prompt)

# Parse JSON response
try:
    result = json.loads(response.content)
    print("Parsed JSON:", result)
except json.JSONDecodeError:
    print("Response:", response.content)
```

### Using with LangChain Chains (LCEL)

```python
from langchain.prompts import FewShotPromptTemplate, PromptTemplate
from langchain_openai import ChatOpenAI

# Setup few-shot template (using previous examples)
few_shot_template = FewShotPromptTemplate(
    examples=examples,
    example_prompt=example_template,
    prefix="You are a medical insurance expert. Use these examples as guidance:",
    suffix="Question: {input}\nAnswer:",
    input_variables=["input"]
)

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.3)

# Create chain using LCEL
chain = few_shot_template | llm

# Invoke chain
response = chain.invoke({"input": "What is a premium?"})
print(response.content)
```

### Dynamic Example Selection

For large example sets, use ExampleSelector to choose relevant examples dynamically:

```python
from langchain.prompts import FewShotPromptTemplate, PromptTemplate
from langchain.prompts.example_selector import SemanticSimilarityExampleSelector
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

# Large example set
examples = [
    {"input": "What is a deductible?", "output": "..."},
    {"input": "What is a copayment?", "output": "..."},
    {"input": "What is coinsurance?", "output": "..."},
    {"input": "What is a premium?", "output": "..."},
    {"input": "What is an EOB?", "output": "..."},
    # ... 20+ more examples
]

# Create semantic selector
example_selector = SemanticSimilarityExampleSelector.from_examples(
    examples,
    OpenAIEmbeddings(),
    FAISS,
    k=3  # Select top 3 most relevant examples
)

# Use with FewShotPromptTemplate
few_shot_template = FewShotPromptTemplate(
    example_selector=example_selector,  # Use selector instead of examples
    example_prompt=example_template,
    prefix="You are a medical insurance expert. Here are relevant examples:",
    suffix="Question: {input}\nAnswer:",
    input_variables=["input"]
)

# Now it automatically picks the 3 most relevant examples
formatted = few_shot_template.format(input="How does insurance work?")
```

---

## Advantages of `from_examples()` (Few-Shot Learning)

### ✅ Pros

1. **Teaches by Demonstration**: Model learns desired format/style from examples without fine-tuning
2. **Consistency**: Produces uniform responses matching example patterns
3. **Domain Adaptation**: Quickly adapts general models to specific domains (medical, legal, technical)
4. **Format Control**: Ensures specific output structures (JSON, tables, bullet points)
5. **Reduced Prompt Engineering**: Less trial-and-error compared to zero-shot prompting
6. **No Fine-Tuning Required**: Works with base models, no training data or compute needed
7. **Contextual Learning**: Model understands task from context alone
8. **Tone and Style**: Examples establish desired communication style
9. **Complex Tasks**: Handles multi-step reasoning or structured outputs better
10. **Cost-Effective**: Cheaper than fine-tuning, scales easily

### Example: Format Enforcement

```python
# Without examples - inconsistent format
prompt = "What is a deductible?"
# Response varies: paragraph, bullets, long/short, etc.

# With examples - consistent format
examples = [
    {"input": "What is X?", "output": "**Definition**: X is...\n**Example**: For instance..."}
]
# All responses follow: Definition + Example structure
```

### Example: Domain Adaptation

```python
# Medical billing expert using insurance terminology
examples = [
    {"input": "Explain CPT code", "output": "CPT (Current Procedural Terminology) codes are..."},
    {"input": "What is ICD-10?", "output": "ICD-10 (International Classification of Diseases) is..."}
]
# Model now uses proper medical billing terminology
```

---

## Limitations of `from_examples()` (Few-Shot Learning)

### ❌ Cons

1. **Token Overhead**: Examples consume prompt tokens, increasing costs and latency
2. **Context Window Limits**: Large example sets may exceed model's context window
3. **Manual Curation**: Requires crafting high-quality examples manually
4. **Example Quality Dependence**: Poor examples lead to poor outputs
5. **Not a Substitute for Fine-Tuning**: For highly specialized tasks, fine-tuning may be better
6. **Maintenance Burden**: Examples need updates as requirements change
7. **Overfitting Risk**: Model may mimic examples too literally, lacking flexibility
8. **Complexity**: More setup compared to simple `from_template()`
9. **Selection Strategy**: Choosing right examples is critical but non-obvious
10. **Debugging Difficulty**: Hard to isolate whether failures are from examples or instructions

### Example: Token Cost Problem

```python
# 10 examples × 100 tokens each = 1,000 tokens
# For 1,000 API calls:
# Input tokens: 1,000,000 (cost: $0.15 for gpt-4o-mini)
# This adds up quickly compared to zero-shot prompts
```

### Example: Context Window Overflow

```python
# gpt-4o-mini context window: 128k tokens
# If you have 500 examples × 200 tokens = 100k tokens just for examples
# Leaves only 28k for actual query and response
# Solution: Use SemanticSimilarityExampleSelector to limit to top 3-5
```

### When NOT to Use `from_examples()`

Use simpler methods when:
- Task is straightforward and model already performs well (zero-shot)
- Token budget is tight
- Examples are hard to create or curate
- Model output variability is acceptable
- You're doing rapid prototyping (use `from_template()` first)

```python
# Simple task - no examples needed
template = PromptTemplate.from_template(
    "Summarize this in 50 words: {text}"
)
# Overkill to provide examples for basic summarization
```

---

## Tech Stack & Installation

### Tech Stack
- **Framework**: FastAPI 0.111.0
- **Server**: Uvicorn 0.30.1
- **Runtime**: Python 3.10+
- **LLM Integration**:
  - **LangChain** 0.3.27
  - **LangChain-OpenAI** 0.3.35
  - **LangChain-Core** >=0.3.78, <1.0.0
  - **LangChain-Community** (for example selectors)
  - **OpenAI Python SDK**
- **Data Validation**: Pydantic

### Installation

```bash
# Install core dependencies
pip install fastapi==0.111.0
pip install uvicorn[standard]==0.30.1
pip install langchain==0.3.27
pip install langchain-openai==0.3.35
pip install "langchain-core>=0.3.78,<1.0.0"
pip install langchain-community
pip install openai
pip install python-dotenv pydantic-settings

# For semantic example selection
pip install faiss-cpu tiktoken
```

### Environment Setup (Windows)

```bash
# Create virtual environment
cd C:\v\v\learn\lv_python\ai\VishAgent\app
python -m venv venv

# Activate
C:\v\v\learn\lv_python\ai\VishAgent\app\venv\Scripts\activate.bat

# Configure .env file
```

Create `.env` file:
```env
ENV=development
OPEN_AI_KEY=sk-proj-your_actual_key_here
OPEN_AI_MODEL_NAME=gpt-4o-mini
APP_NAME=VishAgent
HOST=127.0.0.1
PORT=825
LOG_LEVEL=INFO
```

Get your API key at [OpenAI Platform](https://platform.openai.com/api-keys).

```bash
# Run application
python main.py
```

---

## How to Call OpenAI with FewShotPromptTemplate

### Method 1: Using ChatOpenAI with Few-Shot (Recommended)

```python
from langchain.prompts import FewShotPromptTemplate, PromptTemplate
from langchain_openai import ChatOpenAI
import os

# Define examples
examples = [
    {"question": "What is a deductible?", "answer": "A deductible is the amount you pay before insurance starts covering costs."},
    {"question": "What is a premium?", "answer": "A premium is the monthly payment you make to keep your insurance active."}
]

# Create example template
example_template = PromptTemplate(
    input_variables=["question", "answer"],
    template="Q: {question}\nA: {answer}"
)

# Create few-shot template
few_shot_template = FewShotPromptTemplate(
    examples=examples,
    example_prompt=example_template,
    prefix="You are a medical insurance expert. Use these examples as guidance:",
    suffix="Q: {question}\nA:",
    input_variables=["question"]
)

# Initialize ChatOpenAI
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.3,
    api_key=os.getenv("OPEN_AI_KEY")
)

# Create chain
chain = few_shot_template | llm

# Invoke
response = chain.invoke({"question": "What is coinsurance?"})
print(response.content)
```

### Method 2: Format Then Invoke

```python
# Format first
formatted_prompt = few_shot_template.format(question="What is an EOB?")
print("Formatted Prompt:")
print(formatted_prompt)

# Then invoke
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.3)
response = llm.invoke(formatted_prompt)
print("\nLLM Response:")
print(response.content)
```

### Method 3: With Dynamic Example Selection

```python
from langchain.prompts.example_selector import SemanticSimilarityExampleSelector
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

# Large example set
examples = [
    {"input": "What is a deductible?", "output": "A deductible is..."},
    {"input": "What is a copayment?", "output": "A copayment is..."},
    # ... more examples
]

# Create semantic selector
example_selector = SemanticSimilarityExampleSelector.from_examples(
    examples,
    OpenAIEmbeddings(),
    FAISS,
    k=2  # Select top 2 most relevant
)

# Few-shot with selector
few_shot_template = FewShotPromptTemplate(
    example_selector=example_selector,
    example_prompt=example_template,
    prefix="You are a medical insurance expert. Here are relevant examples:",
    suffix="Q: {input}\nA:",
    input_variables=["input"]
)

llm = ChatOpenAI(model="gpt-4o-mini")
chain = few_shot_template | llm
response = chain.invoke({"input": "How do insurance payments work?"})
```

### Method 4: Streaming Responses

```python
llm = ChatOpenAI(model="gpt-4o-mini", streaming=True)
chain = few_shot_template | llm

# Stream response
for chunk in chain.stream({"question": "What is a health insurance network?"}):
    print(chunk.content, end="", flush=True)
```

---

## Request & Response Structure

### Successful Response Example

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
      "total_tokens": 87
    },
    "model_name": "gpt-4o-mini-2024-07-18",
    "finish_reason": "stop"
  },
  "usage_metadata": {
    "input_tokens": 43,
    "output_tokens": 44,
    "total_tokens": 87
  }
}
```

### Accessing Response Data

```python
response = chain.invoke({"input": "What is a claim?"})

# Access content
print(response.content)

# Access metadata
print(f"Model: {response.response_metadata['model_name']}")
print(f"Total tokens: {response.usage_metadata['total_tokens']}")
```

### Cost Estimation with Few-Shot Examples

```python
def estimate_cost_with_examples(response, num_examples=0, avg_tokens_per_example=50):
    """Estimate cost including few-shot example overhead."""
    input_tokens = response.usage_metadata['input_tokens']
    output_tokens = response.usage_metadata['output_tokens']
    
    example_tokens = num_examples * avg_tokens_per_example
    actual_query_tokens = input_tokens - example_tokens
    
    input_cost = (input_tokens / 1_000_000) * 0.15
    output_cost = (output_tokens / 1_000_000) * 0.60
    
    return {
        "total_tokens": input_tokens + output_tokens,
        "example_overhead_tokens": example_tokens,
        "total_cost_usd": round(input_cost + output_cost, 6)
    }
```

---

## Exception Handling

### 1. Invalid API Key (401)

```python
from openai import AuthenticationError

try:
    llm = ChatOpenAI(model="gpt-4o-mini", api_key=os.getenv("OPEN_AI_KEY"))
    response = llm.invoke("Test")
except AuthenticationError:
    print("❌ Invalid API key. Check .env file")
```

### 2. Missing Example Variables

```python
def validate_examples(examples, required_keys):
    """Validate examples have required keys."""
    for i, example in enumerate(examples):
        missing = set(required_keys) - set(example.keys())
        if missing:
            raise ValueError(f"❌ Example {i} missing: {missing}")
```

### 3. Rate Limit Error (429)

```python
from openai import RateLimitError
import time

def invoke_with_retry(chain, inputs, max_retries=3):
    for attempt in range(max_retries):
        try:
            return chain.invoke(inputs)
        except RateLimitError:
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)
            else:
                raise
```

### 4. Context Length Exceeded

```python
from langchain.prompts.example_selector import LengthBasedExampleSelector

example_selector = LengthBasedExampleSelector(
    examples=large_example_list,
    example_prompt=example_template,
    max_length=2000  # Limit token count
)
```

### 5. Empty Examples

```python
if not examples or len(examples) == 0:
    raise ValueError("❌ Examples cannot be empty")
```

### 6. Placeholder Response

```python
def validate_response(response):
    """Detect placeholder text."""
    if isinstance(response, dict):
        content = response.get("response", "")
        if "will handle requests" in content.lower():
            raise ValueError("❌ Placeholder response detected")
    return True
```

---

## API Endpoints

### GET `/api/api_lc_pt/few_shot_prompt`

Execute few-shot prompt with examples.

**Query Parameters:**
- `question` (required): User's question

**Response:**
```json
{
  "response": {
    "content": "...",
    "tokens": {"total_tokens": 185}
  }
}
```

---

## References

### Official Documentation
- [LangChain FewShotPromptTemplate](https://python.langchain.com/docs/modules/model_io/prompts/few_shot_examples/)
- [Example Selectors](https://python.langchain.com/docs/modules/model_io/prompts/example_selectors/)
- [ChatOpenAI](https://python.langchain.com/docs/integrations/chat/openai)
- [OpenAI API Reference](https://platform.openai.com/docs/api-reference)

### Tutorials
- [Few-Shot Learning Guide](https://www.promptingguide.ai/techniques/fewshot)
- [OpenAI Few-Shot Examples](https://platform.openai.com/docs/guides/prompt-engineering)

### Research
- [GPT-3 Paper - Few-Shot Learners](https://arxiv.org/abs/2005.14165)
- [In-Context Learning Survey](https://arxiv.org/abs/2301.00234)

### Community
- [LangChain Discord](https://discord.gg/langchain)
- [OpenAI Forum](https://community.openai.com/)

---

## Project Structure
```
VishAgent/
├── app/
│   ├── main.py                      # FastAPI entry
│   ├── api/
│   │   ├── router.py
│   │   └── api_pt/
│   │       ├── api_lc_pt.py         # FewShot endpoints
│   │       └── api_lc_pt_01_pt.py
│   ├── core/config.py
│   ├── models/
│   └── services/
├── requirements.txt
├── .env
└── README.md
```

---

## License
Proprietary - VishAgent

**Author:** Vishnu Kiran M  
**Expertise:** AI Solution Designer  
**Date:** January 2026

--- 
