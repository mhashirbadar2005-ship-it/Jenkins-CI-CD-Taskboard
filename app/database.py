import os

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# The database location comes from the environment. Locally it falls back
# to a SQLite file; on the server it points at AWS RDS (PostgreSQL).
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./taskboard.db")

connect_args = {}
if DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

engine = create_engine(DATABASE_URL, pool_pre_ping=True, connect_args=connect_args)
SessionLocal = sessionmaker(bind=engine, autoflush=False)
Base = declarative_base()


def get_db():
    """Give each request its own database session, and always close it."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
