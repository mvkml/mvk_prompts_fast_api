# VishAgent — LangChain ChatPromptTemplate Methods (Focus: from_template)

## Author
Vishnu Kiran M  
Expertise in designing AI solutions

---

## Overview
This guide explains what a PromptTemplate is, outlines the main methods available in LangChain, and provides a focused walkthrough of ChatPromptTemplate.from_template, including advantages, limitations, and how to call OpenAI with proper exception handling.

---

## What is PromptTemplate?

PromptTemplate is a LangChain construct for building parameterized prompts. It helps you:

- Define reusable prompt structures with placeholders
- Inject variables safely without manual string concatenation
- Keep prompts consistent, versionable, and testable
- Compose prompts for chains and agents

LangChain supports both plain PromptTemplate (single string prompts) and ChatPromptTemplate (multi-message chat-style prompts with roles like system/user/assistant).

---

## PromptTemplate Methods

- Constructor: Create with explicit input variables and a template string.
- from_template: Build directly from a string with `{placeholders}`.
- from_file: Load a template from a file (txt, json, yaml) on disk.
- from_examples: Create from example strings (few-shot formatting, typically for PromptTemplate/FewShotPromptTemplate).
- ChatPromptTemplate: Compose multi-message prompts.
  - ChatPromptTemplate.from_messages: Build from a list of role-tagged messages.
  - ChatPromptTemplate.from_template: Build a chat prompt from a single template string (treated as a human/user message).

---

## Focus: ChatPromptTemplate.from_template

### What it does
Creates a chat-style prompt from one template string. This is useful when you want chat semantics (LLM expects chat messages) but your prompt is a single user query enriched with variables.

### Example
```python
from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from app.core.config import settings

# Define a single-message chat prompt using variables
prompt = ChatPromptTemplate.from_template(
	"You are a medical insurance assistant.\n"
	"Question: {question}\n"
	"Answer clearly and professionally in under {words} words."
)

# Create the LLM (aligned to project config)
llm = ChatOpenAI(
	model=settings.open_ai_model_name,
	temperature=0.3,
	openai_api_key=settings.open_ai_key,
)

try:
	# Format the chat prompt into messages consumable by the LLM
	messages = prompt.format_messages(question="What is an EOB?", words=40)
	# Invoke model with chat messages
	msg = llm.invoke(messages)
	print(msg.content)
except Exception as ex:
	print({"error": str(ex)})
```

### With system+user messages (for context)
```python
from langchain.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_messages([
	("system", "You are a medical insurance assistant. Be concise."),
	("user", "Question: {question}\nAnswer in under {words} words."),
])

messages = prompt.format_messages(question="What is coinsurance?", words=35)
```

### Advantages
- Chat-native: Produces structured chat messages for LLMs expecting role-based inputs
- Simplicity: One template string with variables—easy to maintain
- Flexibility: Can be combined later with system/assistant messages if needed

### Limitations
- Single message: from_template creates only one chat message (human/user). Use from_messages to mix system/user/assistant roles
- Variable schema: Placeholder mismatches (e.g., missing `{words}`) only surface at format-time
- Less guidance: Without a system message, you rely on the single user prompt for instruction

---

## Calling OpenAI (Project-Aligned)

Using LangChain’s ChatOpenAI wrapper:
```python
from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from app.core.config import settings

prompt = ChatPromptTemplate.from_template(
	"You are a medical insurance assistant.\n"
	"Question: {question}\n"
	"Answer professionally in under {words} words."
)

llm = ChatOpenAI(
	model=settings.open_ai_model_name,
	temperature=0.3,
	openai_api_key=settings.open_ai_key,
)

try:
	messages = prompt.format_messages(question="Explain UB claim", words=45)
	msg = llm.invoke(messages)
	print(msg.content)
except Exception as ex:
	print({"error": str(ex)})
```

Direct OpenAI SDK (for reference, see `api_pt/api_pt.py` in this project):
```python
from openai import OpenAI
from app.core.config import settings

client = OpenAI(api_key=settings.open_ai_key)

messages = [
	{"role": "system", "content": "You are a helpful AI assistant"},
	{"role": "user", "content": "Explain EOB in 40 words"}
]

try:
	resp = client.chat.completions.create(
		model=settings.open_ai_model_name,
		messages=messages,
		temperature=0.3,
	)
	print(resp.choices[0].message.content)
except Exception as ex:
	print({"error": str(ex)})
```

---

## Exceptions and Good Practices

- Validate placeholders: Ensure all variables used in the template are provided to `format_messages()`
- Use system messages for stable behavior: Prefer `from_messages` with a system message for stronger instruction adherence
- Surface errors predictably: Return JSON `{ "error": "..." }` from API endpoints for clients
- Keep prompts version-controlled: Store templates in code or files, and review changes via PRs

---

## References

- ChatPromptTemplate: https://python.langchain.com/docs/concepts/prompt_templates/#chat-prompt-templates
- LangChain PromptTemplate: https://python.langchain.com/docs/concepts/prompt_templates/
- LangChain OpenAI: https://python.langchain.com/docs/integrations/chat/openai
- OpenAI Chat Completions: https://platform.openai.com/docs/guides/text-generation
