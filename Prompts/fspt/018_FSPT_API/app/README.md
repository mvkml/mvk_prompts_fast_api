# VishAgent - Message Placeholders & MessagesPlaceholder

## What is a Message Placeholder?

A **message placeholder** is a structured format for passing conversation context between different roles in an OpenAI chat completion API call. In the OpenAI API, messages are organized by roles to maintain conversation flow and enable features like function/tool calling.

## Message Roles in OpenAI API

### 1. **System Role**
Defines the AI assistant's behavior and context.
```python
{"role": "system", "content": "You are a helpful AI assistant"}
```

### 2. **User Role**
Contains the user's input, questions, or prompts.
```python
{"role": "user", "content": prompt}
```

### 3. **Assistant Role**
Contains the AI model's responses, including tool calls.
```python
{"role": "assistant", "content": "Response text", "tool_calls": [...]}
```

### 4. **Tool Role**
Returns the result of a tool/function execution back to the model.
```python
{
    "role": "tool",
    "tool_call_id": tool_call.id,
    "content": json.dumps(tool_result)
}
```

## Message Flow Pattern in VishAgent

### Basic Chat Completion
```python
messages = [
    {"role": "system", "content": "You are a helpful AI assistant"},
    {"role": "user", "content": prompt}
]

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=messages,
    temperature=0.3
)
```

### Tool Calling Pattern (3-Step Flow)

#### Step 1: Initial Call with Tools
```python
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": prompt}],
    tools=tools,
    tool_choice="auto"
)
```

#### Step 2: Execute Tool and Format Result
```python
# Extract tool call from response
tool_call = response.choices[0].message.tool_calls[0]

# Execute the function
tool_result = execute_function(tool_call)

# Store result in model placeholder
model.Message = json.dumps(tool_result)
```

#### Step 3: Final Call with Tool Result
```python
final = client.chat.completions.create(
    model="gpt-4o-mini",
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

## Template Placeholders

### Prompt Template Pattern
Templates use `{placeholder}` syntax for dynamic content injection:

```python
PROMPT_TEMPLATE = """
You are an expert medical insurance assistant.

User Question:
{question}

Relevant Context:
{context}

Answer clearly and professionally.
Note: Provide response in max 50 words only
"""

# Format with actual values
prompt = PROMPT_TEMPLATE.format(
    question=question,
    context=context
)
```

---

## What is MessagesPlaceholder?

**MessagesPlaceholder** is a powerful component from **LangChain** that dynamically injects conversation message history into prompt templates. It's a placeholder that gets populated with actual message objects at runtime, enabling flexible conversation management in LangGraph applications.

### Key Characteristics

1. **Dynamic Message Injection**: Automatically includes chat history without hardcoding messages
2. **LangChain Integration**: Works seamlessly with LangChain's PromptTemplate and ChatPromptTemplate
3. **LangGraph Compatibility**: Essential for building agentic workflows with stateful conversation
4. **Flexible Role Handling**: Automatically manages message roles (system, user, assistant, tool)

### Basic Usage Pattern

```python
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI

# Create prompt with MessagesPlaceholder
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful AI assistant"),
    MessagesPlaceholder(variable_name="chat_history"),
    ("user", "{input}")
])

# Initialize LLM
llm = ChatOpenAI(model="gpt-4o-mini")

# Create chain
chain = prompt | llm

# Invoke with message history
response = chain.invoke({
    "chat_history": [
        {"role": "user", "content": "What is Python?"},
        {"role": "assistant", "content": "Python is a programming language..."}
    ],
    "input": "Tell me more about it"
})
```

### Advanced Usage in LangGraph

```python
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langgraph.graph import StateGraph
from typing import Annotated
from langgraph.graph.message import add_messages

# Define state with message list
class AgentState(TypedDict):
    messages: Annotated[list, add_messages]

# Create graph
graph = StateGraph(AgentState)

# Define agent node with MessagesPlaceholder
def agent_node(state):
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful assistant"),
        MessagesPlaceholder(variable_name="messages")
    ])
    
    chain = prompt | llm
    result = chain.invoke({"messages": state["messages"]})
    
    return {"messages": [result]}

graph.add_node("agent", agent_node)
```

### Why Use MessagesPlaceholder?

| Feature | Description |
|---------|-------------|
| **Automatic History Management** | Maintains full conversation context without manual tracking |
| **Separation of Concerns** | Decouples message handling from prompt logic |
| **Flexibility** | Works with any number of messages in any order |
| **Type Safety** | Integrates with LangChain's type system |
| **Scalability** | Handles long conversation threads efficiently |

### Comparison: Manual vs MessagesPlaceholder

#### Manual Approach (❌ Not Recommended)
```python
# Hardcoded, not scalable
messages = [
    {"role": "system", "content": "You are helpful"},
    {"role": "user", "content": user_msg_1},
    {"role": "assistant", "content": assistant_msg_1},
    # Hard to add more messages dynamically
]
```

#### MessagesPlaceholder Approach (✅ Recommended)
```python
# Dynamic, scalable
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are helpful"),
    MessagesPlaceholder(variable_name="messages")  # Injects any number of messages
])

response = prompt | llm.invoke({
    "messages": conversation_history  # Can be any length
})
```

### Common Use Cases in VishAgent

1. **Multi-turn Conversations**: Store and replay full conversation history
2. **Claim Policy Analysis**: Build context from previous interactions
3. **Tool-Based Agents**: Maintain state across tool calls with LangGraph
4. **Weather Agents**: Remember previous queries in conversation flow

### Integration with LangChain Components

```python
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage

# Create dynamic prompt
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an expert on {topic}"),
    MessagesPlaceholder(variable_name="chat_history"),
    ("user", "{input}")
])

# Build message history
chat_history = [
    HumanMessage(content="What is LLM?"),
    AIMessage(content="An LLM is a Large Language Model..."),
]

# Invoke chain
result = (prompt | llm).invoke({
    "topic": "AI",
    "chat_history": chat_history,
    "input": "Can you explain RAG?"
})
```

## Best Practices

1. **Message Serialization**: Use `model_dump_json()` for Pydantic models, not `dict()` or `json()`
   ```python
   model.Message = llm_response.model_dump_json()
   ```

2. **Maintain Message Order**: Keep messages in chronological order to maintain context
   ```python
   messages = [system_msg, user_msg, assistant_msg, tool_msg]
   ```

3. **Tool Call ID Matching**: Always match `tool_call_id` when returning tool results
   ```python
   {"role": "tool", "tool_call_id": tool_call.id, "content": result}
   ```

4. **Context Preservation**: Include previous messages when making follow-up API calls to maintain conversation context

5. **Use MessagesPlaceholder for LangGraph**: When building agentic workflows, prefer MessagesPlaceholder over manual message construction

## Related Files

- [api_pt.py](api/api_pt/api_pt.py) - Basic prompt/message implementation
- [ClaimPolicy.txt](../Documents/ClaimPolicy/ClaimPolicy.txt) - Claim validation flow
- [lan_graph_caluclator.txt](../Documents/ClaimPolicy/Lan_Graph/lan_graph_caluclator.txt) - LangGraph tool calling pattern
 