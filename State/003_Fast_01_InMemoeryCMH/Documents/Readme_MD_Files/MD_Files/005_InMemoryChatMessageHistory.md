# InMemoryChatMessageHistory

## What is InMemoryChatMessageHistory?

`InMemoryChatMessageHistory` is a LangChain utility class that stores chat message history in memory (RAM) during the runtime of an application. It maintains a conversation context by storing a sequence of messages exchanged between users and AI assistants.

## Key Characteristics

### 1. **In-Memory Storage**
- Messages are stored in Python memory structures (lists)
- Data persists only during the application's runtime
- Data is lost when the application stops or restarts

### 2. **Lightweight & Fast**
- No database or file I/O operations required
- Instant read/write access
- Minimal overhead for simple applications

### 3. **Session-Based**
- Typically used with session IDs to maintain separate conversation threads
- Each session has its own isolated message history

## Installation

```bash
pip install langchain-core
# or
pip install langchain
```

## Basic Usage

### Simple Example

```python
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.messages import HumanMessage, AIMessage

# Create a history instance
history = InMemoryChatMessageHistory()

# Add messages
history.add_message(HumanMessage(content="Hello, how are you?"))
history.add_message(AIMessage(content="I'm doing well, thank you! How can I help you today?"))
history.add_message(HumanMessage(content="Tell me about Python"))
history.add_message(AIMessage(content="Python is a high-level programming language..."))

# Retrieve all messages
messages = history.messages
print(f"Total messages: {len(messages)}")

# Clear history
history.clear()
```

### With Session Management

```python
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.messages import HumanMessage, AIMessage

# Dictionary to store multiple session histories
store = {}

def get_session_history(session_id: str) -> InMemoryChatMessageHistory:
    """Get or create chat history for a session."""
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]

# Use with different sessions
session1 = get_session_history("user_123")
session1.add_message(HumanMessage(content="Hello from user 123"))

session2 = get_session_history("user_456")
session2.add_message(HumanMessage(content="Hello from user 456"))

# Each session maintains separate history
print(f"Session 1 messages: {len(session1.messages)}")
print(f"Session 2 messages: {len(session2.messages)}")
```

## Integration with LangChain Runnables

### With RunnableWithMessageHistory

```python
from langchain_openai import ChatOpenAI
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

# Setup
store = {}

def get_session_history(session_id: str) -> InMemoryChatMessageHistory:
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]

# Create prompt with message history placeholder
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful AI assistant."),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{input}")
])

# Create chain
llm = ChatOpenAI(model="gpt-4o-mini")
chain = prompt | llm

# Wrap with message history
chain_with_history = RunnableWithMessageHistory(
    chain,
    get_session_history,
    input_messages_key="input",
    history_messages_key="history"
)

# Use the chain
response = chain_with_history.invoke(
    {"input": "My name is Alice"},
    config={"configurable": {"session_id": "session_001"}}
)

# Follow-up question - history is maintained
response = chain_with_history.invoke(
    {"input": "What's my name?"},
    config={"configurable": {"session_id": "session_001"}}
)
# Response: "Your name is Alice"
```

## API Methods

### Core Methods

```python
history = InMemoryChatMessageHistory()

# Add a single message
history.add_message(HumanMessage(content="Hello"))
history.add_user_message("Hello")  # Convenience method
history.add_ai_message("Hi there")  # Convenience method

# Add multiple messages
history.add_messages([
    HumanMessage(content="Message 1"),
    AIMessage(content="Response 1")
])

# Get all messages
messages = history.messages  # Returns List[BaseMessage]

# Clear all messages
history.clear()
```

## Use Cases

### ✅ Good For:
- **Development & Testing**: Quick prototyping without database setup
- **Short-lived Sessions**: Temporary conversations during app runtime
- **Single-user Applications**: Desktop tools or scripts
- **Demo Applications**: Proof-of-concept implementations
- **Stateless APIs**: When sessions are managed externally

### ❌ Not Suitable For:
- **Production Multi-user Apps**: Data lost on restart
- **Long-term Conversation History**: No persistence across sessions
- **Distributed Systems**: Memory not shared across servers
- **High-availability Systems**: Data loss on server failure

## Limitations

1. **No Persistence**: Data lost when application stops
2. **Memory Constraints**: Large conversations consume RAM
3. **Not Scalable**: Not suitable for load-balanced environments
4. **No Concurrency Safety**: Not thread-safe by default
5. **No Search/Query**: Simple list structure without indexing

## Alternative Chat History Implementations

For production use, consider persistent alternatives:

```python
# Redis-based (recommended for production)
from langchain_community.chat_message_histories import RedisChatMessageHistory

# File-based
from langchain_community.chat_message_histories import FileChatMessageHistory

# SQL-based
from langchain_community.chat_message_histories import SQLChatMessageHistory

# MongoDB-based
from langchain_community.chat_message_histories import MongoDBChatMessageHistory
```

## Complete FastAPI Example

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

app = FastAPI()

# In-memory store for chat histories
chat_histories = {}

def get_session_history(session_id: str) -> InMemoryChatMessageHistory:
    if session_id not in chat_histories:
        chat_histories[session_id] = InMemoryChatMessageHistory()
    return chat_histories[session_id]

# Create LLM chain
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant."),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{input}")
])

llm = ChatOpenAI(model="gpt-4o-mini")
chain = prompt | llm

chain_with_history = RunnableWithMessageHistory(
    chain,
    get_session_history,
    input_messages_key="input",
    history_messages_key="history"
)

class ChatRequest(BaseModel):
    session_id: str
    message: str

class ChatResponse(BaseModel):
    response: str
    session_id: str

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    try:
        response = chain_with_history.invoke(
            {"input": request.message},
            config={"configurable": {"session_id": request.session_id}}
        )
        return ChatResponse(
            response=response.content,
            session_id=request.session_id
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/chat/{session_id}")
async def clear_chat_history(session_id: str):
    if session_id in chat_histories:
        chat_histories[session_id].clear()
        return {"message": f"Chat history cleared for session {session_id}"}
    return {"message": "Session not found"}

@app.get("/chat/{session_id}/history")
async def get_chat_history(session_id: str):
    if session_id not in chat_histories:
        return {"messages": []}
    
    history = chat_histories[session_id]
    messages = [
        {
            "type": msg.type,
            "content": msg.content
        }
        for msg in history.messages
    ]
    return {"session_id": session_id, "messages": messages}
```

## Best Practices

1. **Session Management**: Always use session IDs to separate conversations
2. **Memory Cleanup**: Implement periodic cleanup of old sessions
3. **Size Limits**: Set maximum message count per session to prevent memory overflow
4. **Transition Plan**: Start with InMemory, migrate to persistent storage for production

```python
# Example: Limit message history size
def get_session_history(session_id: str) -> InMemoryChatMessageHistory:
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    
    history = store[session_id]
    
    # Keep only last 20 messages
    if len(history.messages) > 20:
        history.messages = history.messages[-20:]
    
    return history
```

## Summary

`InMemoryChatMessageHistory` is perfect for:
- Development and testing
- Proof-of-concept applications
- Single-user desktop applications
- Learning LangChain concepts

For production applications with multiple users or requiring persistence, use a database-backed chat history implementation like Redis, SQL, or MongoDB.

---

**Related Documentation**:
- [LangChain Chat History Documentation](https://python.langchain.com/docs/modules/memory/chat_messages/)
- [RunnableWithMessageHistory](https://python.langchain.com/docs/expression_language/how_to/message_history)
