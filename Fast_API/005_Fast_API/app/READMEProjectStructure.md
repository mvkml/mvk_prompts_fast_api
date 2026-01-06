






Project structure

Below is the project structure

fastapi-project/
│
├── app/
│   ├── main.py          # Entry point (like Program.cs)
│   │
│   ├── api/             # API layer (Controllers)
│   │   ├── __init__.py
│   │   ├── v1/
│   │   │   ├── __init__.py
│   │   │   ├── routes/
│   │   │   │   ├── health.py
│   │   │   │   └── agent.py
│   │
│   ├── core/            # App configuration
│   │   ├── config.py
│   │   └── security.py
│   │
│   ├── services/        # Business logic
│   │   └── agent_service.py
│   │
│   ├── models/          # Pydantic models (DTOs)
│   │   └── agent.py
│   │
│   ├── repositories/   # DB layer
│   │   └── agent_repo.py
│   │
│   └── utils/
│       └── helpers.py
│
├── tests/               # Unit & integration tests
│
├── requirements.txt
├── .env
├── README.md
└── .gitignore
