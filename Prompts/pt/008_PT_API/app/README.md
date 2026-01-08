# VishAgent — LangChain PromptTemplate Methods (Focus: from_file)

## Author
Vishnu Kiran M  
Expertise in designing AI solutions

---

## Overview
This guide explains what a `PromptTemplate` is, the main ways to create one in LangChain, and provides a focused walkthrough of the `from_file` method, including advantages, limitations, and how to call OpenAI safely with exceptions.

---

## What is PromptTemplate?

`PromptTemplate` is a LangChain construct for building parameterized prompts. It lets you:

- Define reusable prompt structures with placeholders
- Inject variables safely without manual string concatenation
- Keep prompts consistent, versionable, and testable
- Compose prompts for chains and agents

---

## PromptTemplate Methods

- Constructor: Create with explicit input variables and a template string.
- `from_template`: Build directly from a string with `{placeholders}`.
- `from_file`: Load a template from a file (txt, json, yaml) on disk.
- `from_examples`: Create from example strings (few-shot style formatting).
- `ChatPromptTemplate`: Compose multi-message prompts (system/user/assistant).

---

## Focus: `from_file`

### What it does
Loads a template from a file so you can manage prompts as regular text assets alongside your code. This improves readability, version control, and collaboration.

### Example template file (medical_assistant.txt)
```
You are a medical insurance assistant.

Question: {question}
Constraints: Answer clearly and professionally in under {words} words.
```

Place this file under a predictable path, for example: `app/prompts/medical_assistant.txt`.

### Using `from_file` with LangChain
```python
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from app.core.config import settings

def get_llm():
	# Aligned with project config
	return ChatOpenAI(
		model=settings.open_ai_model_name,
		temperature=0.3,
		openai_api_key=settings.open_ai_key,
	)

def build_prompt_from_file(path: str) -> PromptTemplate:
	# path example: "app/prompts/medical_assistant.txt"
	return PromptTemplate.from_file(path)

def ask(question: str, words: int = 50):
	try:
		template = build_prompt_from_file("app/prompts/medical_assistant.txt")
	except FileNotFoundError:
		# Fallback: minimal inline template if the file is missing
		template = PromptTemplate.from_template(
			"You are a medical insurance assistant.\n"
			"Question: {question}\n"
			"Constraints: Answer in under {words} words."
		)

	try:
		prompt_text = template.format(question=question, words=words)
		llm = get_llm()
		msg = llm.invoke(prompt_text)
		return msg.content
	except Exception as ex:
		# Surface errors in a predictable structure for API clients
		return {"error": str(ex)}
```

### Advantages
- Externalized prompts: Clear separation between code and content
- Version control: Review changes to prompts in diffs/PRs
- Reusability: Share the same template across endpoints/services
- Consistency: Single source of truth for prompt wording

### Limitations
- File management: Requires consistent paths and deployment packaging
- Runtime dependency: Missing files cause errors without fallbacks
- No schema: Typos in placeholder names only surface at runtime

---

## Calling OpenAI (Project-Aligned)

This project uses LangChain’s `ChatOpenAI` wrapper and configuration from `settings`. For direct OpenAI client usage, see `api_pt/api_pt.py`, which demonstrates OpenAI’s chat.completions API.

LangChain call pattern:
```python
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from app.core.config import settings

template = PromptTemplate.from_template(
	"You are a medical insurance assistant.\n"
	"Question: {question}\n"
	"Answer in under {words} words."
)

llm = ChatOpenAI(
	model=settings.open_ai_model_name,
	temperature=0.3,
	openai_api_key=settings.open_ai_key,
)

try:
	prompt_text = template.format(question="What is an EOB?", words=40)
	msg = llm.invoke(prompt_text)
	print(msg.content)
except Exception as ex:
	print({"error": str(ex)})
```

OpenAI Python SDK call pattern (as used in `api_pt/api_pt.py`):
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

- Wrap file access with try/except and provide a minimal fallback template.
- Validate placeholders: keep template variables and `format()` keys in sync.
- Surface errors as JSON from API endpoints for predictable client handling.
- Keep prompt files under a known directory (e.g., `app/prompts/`) and include them in deployment artifacts.

---

## References

- LangChain PromptTemplate (core): https://python.langchain.com/docs/concepts/prompt_templates/
- FewShotPromptTemplate: https://python.langchain.com/docs/how_to/few_shot_examples/
- LangChain OpenAI: https://python.langchain.com/docs/integrations/chat/openai
- OpenAI Chat Completions: https://platform.openai.com/docs/guides/text-generation
 