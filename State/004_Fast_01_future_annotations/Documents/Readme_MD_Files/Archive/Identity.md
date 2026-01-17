## Issue
- `Id` is always `0` after inserting `UserEntity` records, even though the SQL table has `Id` defined as `IDENTITY(1,1)`.
- Cause: SQL Server identity metadata was not declared on the SQLAlchemy column, so the ORM cannot fetch the generated value; `Name` length also differed from the DDL (100 vs 50).

## Solution
1) Align the model with the SQL Server identity column using `Identity` and matching lengths:

```python
from sqlalchemy import Integer, String, Identity
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
	pass


class UserEntity(Base):
	__tablename__ = "UserEntity"
	__table_args__ = {"schema": "dbo"}  # optional but recommended for SQL Server

	Id: Mapped[int] = mapped_column(Integer, Identity(start=1, increment=1), primary_key=True)
	UserId: Mapped[int | None] = mapped_column(Integer, nullable=True)
	Name: Mapped[str | None] = mapped_column(String(50), nullable=True)
```

2) Insert without setting `Id`; let SQL Server generate it and commit/flush so SQLAlchemy refreshes the value:

```python
user = UserEntity(UserId=1, Name="test")
session.add(user)
session.commit()  # or session.flush()
print(user.Id)    # now shows the identity value, not 0
```

3) If you must use a different schema, adjust `__table_args__` accordingly. If you still get 0, verify that `IDENTITY_INSERT` is OFF and that `Id` is not being manually assigned in code.
