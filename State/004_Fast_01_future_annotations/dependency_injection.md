# Dependency Injection (DI)
Dependency Injection is a design technique where objects receive the collaborators they need (their *dependencies*) from the outside instead of creating them internally. This keeps code loosely coupled, easier to test, and simpler to replace implementations (e.g., swap a real DB for an in-memory fake).

## Why It Helps
- Decoupling: Classes focus on behavior, not wiring.
- Testability: Swap dependencies with mocks/fakes without changing code.
- Replaceability: Change implementations via configuration (e.g., different repositories).
- Clarity: Object graphs are explicit, not hidden inside constructors.

## Common DI Styles
- **Constructor Injection**: Pass dependencies via `__init__`. Preferred for mandatory dependencies.
- **Setter/Property Injection**: Assign dependencies after construction. Use sparingly for optional/late-bound dependencies.
- **Interface/Protocol Injection**: Provide dependencies through an abstract contract so callers supply implementations that satisfy it.
- **Factory/Provider Injection**: Inject a callable that creates the dependency on demand (useful for scoped resources like DB sessions).
- **Service Locator (anti-pattern)**: Pull dependencies from a global container. Avoid in new code; it hides object graphs and hurts testability.

## Quick Python Example (constructor injection)
```python
class EmailSender:
	def send(self, to, body):
		...


class UserNotifier:
	def __init__(self, email_sender: EmailSender):
		self.email_sender = email_sender

	def notify(self, user_email, message):
		self.email_sender.send(user_email, message)


# Wiring
email_sender = EmailSender()
notifier = UserNotifier(email_sender)
```

## FastAPI Example (dependency providers)
```python
from fastapi import Depends, FastAPI


class Repository:
	def get_items(self):
		return ["a", "b"]


def get_repo():
	return Repository()


app = FastAPI()


@app.get("/items")
def list_items(repo: Repository = Depends(get_repo)):
	return repo.get_items()
```

## Profile
- Name: [Your Name]
- Role: [Your Role/Title]
- Focus: [e.g., FastAPI, LangGraph, OpenAI tool calling]
- Contact: [Email/LinkedIn]
- Highlights: [Key achievements or interests]
