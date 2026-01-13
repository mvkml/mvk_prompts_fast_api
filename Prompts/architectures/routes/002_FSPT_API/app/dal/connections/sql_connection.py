from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,Session
from app.core.config import settings


SQL_CONNECTION = (
    "mssql+pyodbc://@"
    "(localdb)\\MSSQLLocalDB/MCP_ACRS"
    "?driver=ODBC+Driver+18+for+SQL+Server"
    "&Trusted_Connection=yes"
    "&TrustServerCertificate=yes"
)

engine = create_engine(SQL_CONNECTION,
                       pool_pre_ping=True,
                        future=True)

SessionLocal = sessionmaker(
                            bind=engine,
                            autoflush=False,
                            autocommit=False,
                            future=True
                            )


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    # except Exception as ex:
    #     raise ex
    finally:
        db.close()