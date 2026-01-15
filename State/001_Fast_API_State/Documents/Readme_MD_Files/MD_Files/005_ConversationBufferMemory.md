# ConversationBufferMemory (LangChain)

## Developer Profile

**Name:** Vishnu Kiran M  
**Role:** End-to-End AI, Cloud & Big Data Solution Designer  
**Project:** VishAgent - MARVISH Industrial AI Assistant

---

## What Is ConversationBufferMemory?

ConversationBufferMemory is a LangChain memory component that stores the full history of a conversation in a simple buffer (ordered list of messages) and feeds that history back to the LLM on each turn. It’s the most straightforward way to enable multi-turn, context-aware chats.

- **Purpose:** Preserve prior user/assistant messages so the model can respond with context.
- **Storage model:** In-memory buffer (FIFO list); no automatic truncation.
- **Format:** Returns the conversation as a single string or structured messages, depending on configuration.
- **Best for:** Short to medium conversations where full history fits within the model’s context window.

---

## How It Works

- On each request, the memory returns all prior messages combined as a context string (or messages) to the LLM.
- After the LLM responds, the new user input and assistant output are appended to the buffer.
- No summarization or semantic retrieval is performed (that’s handled by other memory types).

---

## Basic Usage (LangChain)

```python
from langchain_openai import ChatOpenAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory

# 1) LLM with tool support in LangChain
llm = ChatOpenAI(model="gpt-4.1-mini", temperature=0.3)

# 2) Create a plain buffer memory
memory = ConversationBufferMemory(return_messages=True)

# 3) Build a conversation chain that injects memory automatically
conversation = ConversationChain(
		llm=llm,
		memory=memory,
		verbose=True,
)

# 4) Use it in a loop or API
print(conversation.predict(input="What is claim eligibility?"))
print(conversation.predict(input="Summarize our discussion in 1 line."))
```

Notes:
- `return_messages=True` keeps the history as role-tagged messages instead of one big string (often more flexible).
- Use a small `temperature` for deterministic, professional responses in enterprise flows.

---

## With FastAPI (VishAgent-Style Endpoint)

```python
# app snippet
from fastapi import APIRouter
from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory

router = APIRouter()

class ChatRequest(BaseModel):
		session_id: str
		message: str

# Simple in-memory store (swap to Redis/DB for production)
sessions = {}

def get_or_create_chain(session_id: str) -> ConversationChain:
		if session_id not in sessions:
				llm = ChatOpenAI(model="gpt-4.1-mini", temperature=0.3)
				memory = ConversationBufferMemory(return_messages=True)
				sessions[session_id] = ConversationChain(llm=llm, memory=memory)
		return sessions[session_id]

@router.post("/chat")
async def chat(req: ChatRequest):
		chain = get_or_create_chain(req.session_id)
		reply = chain.predict(input=req.message)
		return {"session_id": req.session_id, "reply": reply}
```

Tips:
- Replace the `sessions` dict with Redis or DB-backed memory to scale beyond a single process.
- Add authentication and rate limiting in production.

---

## When To Use It

- **Use ConversationBufferMemory if:**
	- Conversations are relatively short and must include all prior turns.
	- You want the simplest, most transparent behavior (no summaries, no retrieval).
	- You’re prototyping or building internal tools.

- **Consider alternatives if:**
	- Chats get long and exceed the model context window → use ConversationSummaryMemory or ConversationalBufferWindowMemory.
	- You need knowledge-grounding beyond chat history → add RetrievalQA/semantic memory (vector DB).
	- You want a hybrid approach → combine buffer for recency + summary for older context.

---

## Common Variants (Compare)

- **ConversationBufferMemory:**
	- Pros: Simple, preserves exact wording, zero extra compute.
	- Cons: Can overflow model context with long chats.

- **ConversationSummaryMemory:**
	- Pros: Summarizes older parts to stay within context limits.
	- Cons: Loses exact phrasing; extra LLM calls for summaries.

- **ConversationalBufferWindowMemory:**
	- Pros: Keeps only the N most recent turns.
	- Cons: Older context is dropped entirely.

- **Vector/Retrieval-Augmented Memory:**
	- Pros: Long-term recall via embeddings; scalable knowledge.
	- Cons: Requires a vector store and retrieval wiring.

---

## Practical Tips

- **Guard the context window:**
	- If messages grow, trim or switch to summary/window memory.
- **Log and inspect:**
	- Periodically log memory size and token usage to avoid spikes.
- **Persistence:**
	- For multi-instance deployments, persist memory (Redis/DB) keyed by `session_id`.
- **Privacy:**
	- Redact PII before storing history; set TTL for ephemeral conversations.

---

## Minimal Swap: Buffer → Window

```python
from langchain.memory import ConversationalBufferWindowMemory

memory = ConversationalBufferWindowMemory(k=6, return_messages=True)
# Keeps only the last 6 exchanges; safer for long sessions.
```

---

## Summary

- **What:** ConversationBufferMemory is a full-history, in-memory buffer for multi-turn chat.
- **Why:** Enables context-aware replies with minimal setup.
- **When:** Short-to-medium conversations, prototyping, or simple assistants.
- **Scale:** For longer chats, use summary or window memory; for knowledge, add retrieval.

---

**Last Updated:** January 15, 2026  
**Project:** VishAgent - MARVISH Industrial AI Assistant  
**Developer:** Vishnu Kiran M

 