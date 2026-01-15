# Connect to SQL Server (Python + SQLAlchemy)

## Connection String
- Format: `mssql+pyodbc://<user>:<password>@<host>:<port>/<database>?driver=ODBC+Driver+17+for+SQL+Server`
- Example: `mssql+pyodbc://sa:Passw0rd@127.0.0.1:1433/MyDb?driver=ODBC+Driver+17+for+SQL+Server`
- Escape special chars in password or use env vars.

## Install Drivers
- Python deps: `pip install sqlalchemy pyodbc`
- Windows ODBC driver: install "ODBC Driver 17 for SQL Server" or newer.

## Minimal Engine Setup
```python
from sqlalchemy import create_engine, text

conn_str = "mssql+pyodbc://sa:Passw0rd@127.0.0.1:1433/MyDb?driver=ODBC+Driver+17+for+SQL+Server"
engine = create_engine(conn_str)

with engine.connect() as conn:
	result = conn.execute(text("SELECT 1"))
	print(result.scalar())
```

## Using Session (SQLAlchemy ORM)
```python
from sqlalchemy.orm import sessionmaker

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

def get_session():
	with SessionLocal() as session:
		yield session
```

## Common Tips
- Ensure the database name exists and the login has rights.
- If using Windows Auth: `mssql+pyodbc://@<host>/<db>?driver=ODBC+Driver+17+for+SQL+Server;Trusted_Connection=yes`.
- For Docker SQL Server, default port is 1433; expose it and allow TCP.
- Test connectivity with `sqlcmd` or Azure Data Studio if Python fails.

## Profile
- Name: [Your Name]
- Role: [Your Role/Title]
- Focus: [e.g., FastAPI, LangGraph, OpenAI tool calling]
- Contact: [Email/LinkedIn]
- Highlights: [Key achievements or interests]
