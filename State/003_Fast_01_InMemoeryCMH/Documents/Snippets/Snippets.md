# VishAgent Code Snippets Documentation

## What Are Code Snippets?

**Code snippets** are reusable chunks of code that solve common problems or implement frequently-used patterns. In VS Code, snippets enable rapid code generation through shortcuts, improving productivity and consistency.

## Benefits of Code Snippets

1. **Faster Development**: Type a shortcut and generate complete code blocks
2. **Consistency**: Ensures uniform code style across the project
3. **Error Reduction**: Pre-tested patterns reduce bugs
4. **Learning Tool**: Reference for common patterns and best practices
5. **Onboarding**: Helps new developers understand project conventions

---

## VishAgent Snippet Files

### 1. **key_binding.json**
Defines keyboard shortcuts for frequently used VS Code commands and snippets.

**Purpose**: Speed up workflow by reducing mouse/menu usage

**Example Key Bindings**:
```json
{
  "key": "ctrl+alt+n",
  "command": "workbench.action.newUntitledFile"
}
```

### 2. **type_except.json**
Type hints and exception handling patterns for Python code.

**Purpose**: Standardize error handling and type annotations across the project

---

## Common VishAgent Snippets

### FastAPI Endpoint Snippet

**Trigger**: `fapi-endpoint`

```python
@router.post("/{endpoint_name}")
async def {function_name}(request: {RequestModel}) -> {ResponseModel}:
    """
    {Endpoint description}
    
    Args:
        request: {RequestModel} containing required data
        
    Returns:
        {ResponseModel} with operation status
    """
    response = {ResponseModel}()
    
    try:
        # Business logic here
        
        response.Message = "Operation successful"
        return response
        
    except Exception as ex:
        response.IsInvalid = True
        response.Message = {"error": str(ex)}
        return response
```

### Service Layer Snippet

**Trigger**: `service-class`

```python
from app.repositories.{entity}_dal import {Entity}DAL
from app.models.{entity} import {Entity}, {Entity}Request

class {Entity}Service:
    """Business logic service for {Entity}."""
    
    def __init__(self, dal: {Entity}DAL):
        self.dal = dal
    
    async def create_{entity}(self, request: {Entity}Request) -> {Entity}:
        """Create {entity} with business logic validation."""
        try:
            # Validation logic
            
            # Call DAL
            result = await self.dal.create_{entity}(request)
            
            return result
        except Exception as ex:
            raise ValueError(f"Error creating {entity}: {str(ex)}")
    
    async def get_{entity}(self, {entity}_id: int) -> {Entity}:
        """Retrieve {entity} with processing."""
        result = await self.dal.get_{entity}_by_id({entity}_id)
        if not result:
            raise ValueError(f"{Entity} {{{entity}_id}} not found")
        return result
```

### DAL (Repository) Snippet

**Trigger**: `dal-class`

```python
from typing import Optional, List
from app.models.{entity} import {Entity}, {Entity}Request
from app.core.database import Database

class {Entity}DAL:
    """Data Access Layer for {Entity} operations."""
    
    def __init__(self, database: Database):
        self.database = database
    
    # CREATE
    async def create_{entity}(self, {entity}_request: {Entity}Request) -> {Entity}:
        """Create a new {entity}."""
        query = """
            INSERT INTO {table_name} (column1, column2)
            VALUES (%s, %s)
            RETURNING *
        """
        result = await self.database.fetch_one(
            query,
            ({entity}_request.field1, {entity}_request.field2)
        )
        return {Entity}(**result)
    
    # READ
    async def get_{entity}_by_id(self, {entity}_id: int) -> Optional[{Entity}]:
        """Retrieve {entity} by ID."""
        query = "SELECT * FROM {table_name} WHERE id = %s"
        result = await self.database.fetch_one(query, ({entity}_id,))
        return {Entity}(**result) if result else None
    
    async def get_all_{entities}(self) -> List[{Entity}]:
        """Retrieve all {entities}."""
        query = "SELECT * FROM {table_name} ORDER BY created_at DESC"
        results = await self.database.fetch(query)
        return [{Entity}(**row) for row in results]
    
    # UPDATE
    async def update_{entity}(self, {entity}_id: int, {entity}_request: {Entity}Request) -> Optional[{Entity}]:
        """Update {entity}."""
        query = """
            UPDATE {table_name}
            SET column1 = %s, column2 = %s
            WHERE id = %s
            RETURNING *
        """
        result = await self.database.fetch_one(
            query,
            ({entity}_request.field1, {entity}_request.field2, {entity}_id)
        )
        return {Entity}(**result) if result else None
    
    # DELETE
    async def delete_{entity}(self, {entity}_id: int) -> bool:
        """Delete {entity} by ID."""
        query = "DELETE FROM {table_name} WHERE id = %s"
        result = await self.database.execute(query, ({entity}_id,))
        return result.rowcount > 0
```

### Pydantic Model Snippet

**Trigger**: `pydantic-model`

```python
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class {ModelName}(BaseModel):
    """Pydantic model for {ModelName}."""
    
    id: Optional[int] = None
    field1: str = Field(..., description="Field description")
    field2: Optional[str] = Field(None, description="Optional field")
    created_at: Optional[datetime] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "field1": "value1",
                "field2": "value2",
                "created_at": "2024-01-01T00:00:00"
            }
        }

class {ModelName}Request(BaseModel):
    """Request model for creating/updating {ModelName}."""
    
    field1: str = Field(..., description="Required field")
    field2: Optional[str] = Field(None, description="Optional field")

class {ModelName}Response(BaseModel):
    """Response model for {ModelName} operations."""
    
    IsInvalid: bool = False
    Message: Optional[str | dict] = None
    Data: Optional[{ModelName}] = None
```

### LangChain Tool Snippet

**Trigger**: `langchain-tool`

```python
from langchain_core.tools import tool
from typing import Union

@staticmethod
@tool
def {tool_name}(param1: float, param2: float) -> Union[float, str]:
    """
    {Tool description}
    
    Args:
        param1: {Description of parameter 1}
        param2: {Description of parameter 2}
    
    Returns:
        Union[float, str]: Result of operation
    """
    try:
        result = param1 + param2  # Replace with actual logic
        return result
    except Exception as e:
        return f"Error: {str(e)}"
```

### LangGraph StateGraph Snippet

**Trigger**: `langgraph-state`

```python
from langgraph.graph import StateGraph
from langgraph.graph.message import add_messages
from typing import Annotated, TypedDict
from langchain_core.messages import BaseMessage
from langchain_openai import ChatOpenAI

class AgentState(TypedDict):
    """State definition for LangGraph."""
    messages: Annotated[list[BaseMessage], add_messages]
    input: str
    output: str

def create_agent_graph():
    """Create and compile the agent graph."""
    
    # Initialize graph
    graph = StateGraph(AgentState)
    
    # Define nodes
    def agent_node(state):
        llm = ChatOpenAI(model="gpt-4o-mini")
        result = llm.invoke(state["messages"])
        return {"messages": [result]}
    
    def process_node(state):
        # Process LLM output
        return {"output": state["messages"][-1].content}
    
    # Add nodes to graph
    graph.add_node("agent", agent_node)
    graph.add_node("process", process_node)
    
    # Add edges
    graph.add_edge("agent", "process")
    graph.set_entry_point("agent")
    graph.set_finish_point("process")
    
    # Compile
    compiled_graph = graph.compile()
    return compiled_graph
```

### Exception Handling Snippet

**Trigger**: `try-except-handler`

```python
try:
    # Main operation
    result = await operation()
    
except ValueError as ve:
    # Handle validation errors
    logger.error(f"Validation error: {str(ve)}")
    response.IsInvalid = True
    response.Message = {"error": f"Validation: {str(ve)}"}
    return response
    
except Exception as ex:
    # Handle unexpected errors
    logger.error(f"Unexpected error: {str(ex)}", exc_info=True)
    response.IsInvalid = True
    response.Message = {"error": "Internal server error"}
    return response
```

### Async Database Query Snippet

**Trigger**: `async-db-query`

```python
async def {operation_name}(self, {param}: {type}) -> Optional[{Model}]:
    """
    {Operation description}
    
    Args:
        {param}: {Parameter description}
    
    Returns:
        Optional[{Model}]: Result or None if not found
    """
    query = """
        SELECT * FROM {table_name}
        WHERE {condition} = %s
    """
    
    try:
        result = await self.database.fetch_one(query, ({param},))
        return {Model}(**result) if result else None
    except Exception as ex:
        logger.error(f"Database error: {str(ex)}")
        raise
```

### Logging Snippet

**Trigger**: `logger-setup`

```python
import logging

# Configure logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Create handler
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

# Usage
logger.info(f"Operation started: {operation_name}")
logger.warning(f"Warning: {message}")
logger.error(f"Error occurred: {error_message}", exc_info=True)
```

---

## How to Use Snippets in VS Code

### Method 1: Using Trigger Shortcuts
```
1. Open a Python file
2. Press Ctrl+Space to open IntelliSense
3. Type the snippet trigger (e.g., "fapi-endpoint")
4. Press Tab or Enter to insert
5. Use Tab to navigate between placeholders
```

### Method 2: Installing Custom Snippets
```
1. Go to File → Preferences → User Snippets
2. Select "python" or create a new snippet file
3. Add your snippet definitions
4. Use the format below:
```

### Snippet Definition Format
```json
{
  "Endpoint": {
    "prefix": "fapi-endpoint",
    "body": [
      "@router.post(\"/${1:path}\")",
      "async def ${2:function_name}(request: ${3:RequestModel}) -> ${4:ResponseModel}:",
      "    response = ${4:ResponseModel}()",
      "    try:",
      "        ${5:# Business logic}",
      "        return response",
      "    except Exception as ex:",
      "        response.IsInvalid = True",
      "        response.Message = {\"error\": str(ex)}",
      "        return response"
    ],
    "description": "FastAPI endpoint template"
  }
}
```

---

## VishAgent Snippet Conventions

### Naming Convention
```
{layer}-{entity/concept}

Examples:
- fapi-endpoint      (FastAPI endpoint)
- service-class      (Service class)
- dal-class          (Data Access Layer)
- langchain-tool     (LangChain tool)
- pydantic-model     (Pydantic model)
```

### Placeholder Convention
```
${1:PlaceholderName}  - Placeholder with tab order
${1|option1,option2|} - Choice between options
$0                     - Final cursor position
```

### Documentation Requirements
Every snippet should include:
- **Description**: What the snippet does
- **Use Case**: When to use it
- **Placeholders**: Explanation of variables
- **Example**: Complete working example

---

## Best Practices for Snippets

1. **Keep Snippets DRY**: Don't duplicate code between snippets
2. **Include Documentation**: Always add docstrings and comments
3. **Use Proper Indentation**: Maintain consistent code style
4. **Test Before Sharing**: Ensure snippet generates valid code
5. **Version Control**: Keep snippets in Git for team consistency
6. **Regular Updates**: Update snippets as patterns evolve
7. **Clear Naming**: Use intuitive trigger names

---

## VishAgent Project Integration

### Snippet Locations
```
Documents/Snippets/
├── Snippets.md              (This file)
├── key_binding.json         (Keyboard shortcuts)
├── type_except.json         (Type hints & exceptions)
└── custom_snippets.json     (Project-specific snippets)
```

### Setting Up Snippets for Your Team

**Step 1**: Create `.vscode/snippets/python.json`
```bash
mkdir -p .vscode/snippets
touch .vscode/snippets/python.json
```

**Step 2**: Add VishAgent snippets
```json
{
  "VishAgent FastAPI Endpoint": {
    "prefix": "va-endpoint",
    "body": [ ... ],
    "description": "VishAgent FastAPI endpoint pattern"
  }
}
```

**Step 3**: Share with team via Git
```bash
git add .vscode/snippets/
git commit -m "Add VishAgent code snippets"
```

---

## Related Files

- [key_binding.json](key_bindnig.json) - Keyboard shortcuts
- [type_except.json](type_except.json) - Type hints & exception patterns
- [README.md](../../app/README.md) - Main project documentation
- [READMEProjectStructure.md](../../app/READMEProjectStructure.md) - Architecture guide
