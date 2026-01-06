# VishAgent - MARVISH Industrial AI Assistant

FastAPI-based AI agent system for claim policy analysis and LLM tool calling using OpenAI and LangGraph.

## 🏗️ Architecture

```
api/v1/routes/ → core/ → services/ → models/ → repositories/ → utils/
```

**Current Implementation:**
- FastAPI application running on port 825
- API router structure with modular endpoint organization
- Integration with OpenAI GPT-4 for LLM operations
- LangGraph for tool-calling workflows
- Pydantic models for request/response validation

**Planned Features:**
- Complete layered architecture implementation
- Claim policy validation services
- Advanced LLM provider abstractions

## 🚀 Quick Start

### 1. Setup Virtual Environment

```bash
# Navigate to project app directory
cd C:\v\v\learn\lv_python\ai\VishAgent\app

# Create virtual environment
python -m venv venv

# Activate (Windows - use full path for reliability)
C:\v\v\learn\lv_python\ai\VishAgent\app\venv\Scripts\activate.bat
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

**Core Dependencies:**
- `fastapi==0.111.0` - Web framework
- `uvicorn[standard]==0.30.1` - ASGI server

**LangGraph Dependencies (if using):**
```bash
pip install langchain==0.3.27
pip install "langchain-core>=0.3.78,<1.0.0"
pip install langchain-openai==0.3.35
pip install langgraph
```

⚠️ **Important:** Keep `langchain-core` at `0.3.x` (NOT `1.x`) for compatibility.

### 3. Run the Application

```bash
cd C:\v\v\learn\lv_python\ai\VishAgent\app
python main.py
```

The server will start on `http://127.0.0.1:825`

### 4. Access API Documentation

- **Root endpoint:** http://127.0.0.1:825/
- **Swagger UI:** http://127.0.0.1:825/docs
- **ReDoc UI:** http://127.0.0.1:825/redoc
- **OpenAPI JSON:** http://127.0.0.1:825/openapi.json

## 📁 Project Structure

```
app/
├── main.py                 # FastAPI entry point (port 825)
├── api/
│   ├── router.py          # Main router aggregator
│   └── api_pt/            # API endpoints module
│       └── api_pt.py      # Primary router
├── v1/
│   └── models/            # Pydantic DTOs
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

See [READMEProjectStructure.md](READMEProjectStructure.md) for detailed architecture.

## 🔧 Development

### Adding New Endpoints

1. Create route file in `api/api_pt/` or `api/v1/routes/`
2. Define Pydantic models in `v1/models/`
3. Implement business logic in `services/`
4. Register router in `api/router.py`

### LLM Tool Calling Pattern

```python
# 1. Initial call with tools
response = client.chat.completions.create(
    model="gpt-4.1-mini",
    messages=[{"role": "user", "content": prompt}],
    tools=tools,
    tool_choice="auto"
)

# 2. Execute tool and get result
tool_result = execute_function(tool_call)

# 3. Final call with tool result
final = client.chat.completions.create(
    model=model.model_name,
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

### LangGraph Tool Definition (Critical)

```python
# ✅ CORRECT - Use @staticmethod with @tool
@staticmethod
@tool
def tool_add(x: float, y: float) -> float:
    """Add two numbers."""
    return x + y

# ❌ WRONG - Instance method won't work
@tool
def tool_add(self, x: float, y: float) -> float:
    return x + y
```

### Pydantic Serialization

```python
# ✅ Use model_dump_json() for serialization
json_str = tool_schema.model_dump_json()
model.Message = llm_response.model_dump_json()

# ❌ Don't use deprecated methods
# model.dict()  # Old
# model.json()  # Old
```

## 🔗 Related Resources

- **Documentation:** `Documents/` folder
- **Architecture Diagrams:** `Documents/Visio/`
- **Work Documentation:** [Google Drive](https://drive.google.com/drive/folders/1M1cJUJCc1G8iBfmwXUbcX8jtQMG-0-m2)
- **Related Project:** MCPBot (shared patterns)

## ⚙️ Configuration

### Environment Variables
Create `.env` file in `app/` directory:
```
OPENAI_API_KEY=your_api_key_here
```

### Port Configuration
Default development port: `825` (configured in [main.py](main.py))

Production port: `802` (per documentation)

## 🐛 Debugging

### VS Code Debug Setup

Create `.vscode/` directory in the project root with the following configuration files:

#### 1. Create `launch.json` (Debug Configurations)

```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "FastAPI: Debug Server",
            "type": "debugpy",
            "request": "launch",
            "module": "uvicorn",
            "args": [
                "main:app",
                "--host", "127.0.0.1",
                "--port", "825",
                "--reload"
            ],
            "cwd": "${workspaceFolder}/app",
            "env": {
                "PYTHONPATH": "${workspaceFolder}/app"
            },
            "console": "integratedTerminal",
            "justMyCode": true,
            "serverReadyAction": {
                "pattern": "Uvicorn running on (https?://[^\\s]+)",
                "uriFormat": "%s",
                "action": "openExternally"
            }
        },
        {
            "name": "Python: Debug Current File",
            "type": "debugpy",
            "request": "launch",
            "program": "${file}",
            "console": "integratedTerminal",
            "cwd": "${workspaceFolder}/app",
            "env": {
                "PYTHONPATH": "${workspaceFolder}/app"
            },
            "justMyCode": true
        },
        {
            "name": "Python: Attach to Running Server",
            "type": "debugpy",
            "request": "attach",
            "connect": {
                "host": "localhost",
                "port": 5678
            },
            "pathMappings": [
                {
                    "localRoot": "${workspaceFolder}/app",
                    "remoteRoot": "."
                }
            ]
        }
    ]
}
```

#### 2. Create `settings.json` (Workspace Settings)

```json
{
    "python.defaultInterpreterPath": "${workspaceFolder}/app/venv/Scripts/python.exe",
    "python.terminal.activateEnvironment": true,
    "python.analysis.extraPaths": [
        "${workspaceFolder}/app"
    ],
    "python.envFile": "${workspaceFolder}/app/.env",
    
    // Linting & Formatting
    "python.linting.enabled": true,
    "python.linting.pylintEnabled": false,
    "python.linting.flake8Enabled": true,
    "python.formatting.provider": "black",
    
    // Editor
    "editor.formatOnSave": true,
    "editor.codeActionsOnSave": {
        "source.organizeImports": "explicit"
    },
    
    // Files
    "files.exclude": {
        "**/__pycache__": true,
        "**/*.pyc": true
    },
    
    // FastAPI specific
    "files.associations": {
        "*.env": "properties"
    }
}
```

#### 3. Create `tasks.json` (Build/Run Tasks) - Optional

```json
{
    "version": "2.0.0",
    "tasks": [
        {
            "label": "Run FastAPI Server",
            "type": "shell",
            "command": "${workspaceFolder}/app/venv/Scripts/python.exe",
            "args": [
                "-m",
                "uvicorn",
                "main:app",
                "--host", "127.0.0.1",
                "--port", "825",
                "--reload"
            ],
            "options": {
                "cwd": "${workspaceFolder}/app"
            },
            "problemMatcher": [],
            "presentation": {
                "reveal": "always",
                "panel": "new"
            },
            "group": {
                "kind": "build",
                "isDefault": true
            }
        },
        {
            "label": "Install Requirements",
            "type": "shell",
            "command": "${workspaceFolder}/app/venv/Scripts/pip.exe",
            "args": [
                "install",
                "-r",
                "requirements.txt"
            ],
            "options": {
                "cwd": "${workspaceFolder}/app"
            },
            "problemMatcher": []
        }
    ]
}
```

#### 4. Create `extensions.json` (Recommended Extensions) - Optional

```json
{
    "recommendations": [
        "ms-python.python",
        "ms-python.vscode-pylance",
        "ms-python.debugpy",
        "ms-python.black-formatter",
        "charliermarsh.ruff",
        "njpwerner.autodocstring",
        "visualstudioexptteam.vscodeintellicode"
    ]
}
```

### Debugging Steps

#### Method 1: Debug with F5 (Recommended)

1. **Activate Virtual Environment:**
   ```bash
   C:\v\v\learn\lv_python\ai\VishAgent\app\venv\Scripts\activate.bat
   ```

2. **Open VS Code in project folder:**
   ```bash
   cd C:\v\v\learn\lv_python\ai\VishAgent
   code .
   ```

3. **Set Breakpoints:**
   - Open [main.py](main.py) or any API file
   - Click left margin to set breakpoints (red dot)

4. **Start Debugging:**
   - Press `F5` or click "Run and Debug" icon
   - Select **"FastAPI: Debug Server"** configuration
   - Server starts on http://127.0.0.1:825

5. **Test API:**
   - Navigate to http://127.0.0.1:825/docs
   - Make API requests
   - Debugger will pause at breakpoints

6. **Debug Controls:**
   - `F5` - Continue
   - `F10` - Step Over
   - `F11` - Step Into
   - `Shift+F11` - Step Out
   - `Ctrl+Shift+F5` - Restart
   - `Shift+F5` - Stop

#### Method 2: Debug with `debugpy` (Attach Mode)

1. **Install debugpy:**
   ```bash
   pip install debugpy
   ```

2. **Modify [main.py](main.py) to enable remote debugging:**
   ```python
   import debugpy
   
   # Enable debugpy on port 5678
   debugpy.listen(("0.0.0.0", 5678))
   print("⏳ Waiting for debugger attach...")
   debugpy.wait_for_client()
   print("✅ Debugger attached!")
   ```

3. **Run server normally:**
   ```bash
   python main.py
   ```

4. **Attach debugger from VS Code:**
   - Press `F5`
   - Select **"Python: Attach to Running Server"**

#### Method 3: Debug with Uvicorn Directly

```bash
# Navigate to app directory
cd C:\v\v\learn\lv_python\ai\VishAgent\app

# Run with Python debugger
python -m debugpy --listen 5678 --wait-for-client -m uvicorn main:app --host 127.0.0.1 --port 825 --reload
```

### Debugging Tips

**Common Issues:**

1. **Import errors:** Ensure `PYTHONPATH` includes `app/` directory
2. **Virtual environment not active:** Check status bar shows correct Python interpreter
3. **Port already in use:** Kill process on port 825:
   ```bash
   netstat -ano | findstr :825
   taskkill /PID <PID> /F
   ```

**Best Practices:**

- Use `justMyCode: true` to skip library code (toggle with `Ctrl+Shift+F5`)
- Add log statements with `print()` or `logging` module
- Use VS Code Debug Console to evaluate expressions during debugging
- Set conditional breakpoints (right-click breakpoint → Edit Breakpoint)
- Use logpoints for non-intrusive logging (right-click margin → Add Logpoint)

**Environment Variables in Debug:**

Add to `launch.json` → `env` section:
```json
"env": {
    "PYTHONPATH": "${workspaceFolder}/app",
    "OPENAI_API_KEY": "your_key_here",
    "DEBUG": "True"
}
```

**Debugging LangGraph Workflows:**

- Set breakpoints in tool definitions
- Use Debug Console to inspect graph state
- Enable verbose logging:
  ```python
  import logging
  logging.basicConfig(level=logging.DEBUG)
  ```

## 🧪 Testing

```bash
# Run tests (when implemented)
pytest tests/
```

## 📝 Notes

- Project uses Windows-specific paths and activation scripts
- Transitioning from MCPBot patterns
- Documentation-driven development approach
- LangGraph requires specific version constraints

## 👤 Author

**VISHNU KIRAN M**
Industrial AI Assistant Development

---

For detailed AI coding instructions, see [.github/copilot-instructions.md](../.github/copilot-instructions.md)



.vscode/
├── launch.json     👈 Debug configs
├── settings.json   👈 Editor & environment settings
├── tasks.json      👈 Build / run tasks (optional)
├── extensions.json 👈 Recommended extensions (optional)


