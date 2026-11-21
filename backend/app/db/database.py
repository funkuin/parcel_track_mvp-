from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

# Determine connection arguments based on database dialect
connect_args = {}
if settings.DATABASE_URL.startswith("sqlite"):
    # SQLite requires check_same_thread=False for multi-threaded access in FastAPI
    connect_args["check_same_thread"] = False

# Create the SQLAlchemy database engine
engine = create_engine(
    settings.DATABASE_URL,
    connect_args=connect_args,
    echo=False,
)

# Enable foreign key constraint enforcement on SQLite connections
if settings.DATABASE_URL.startswith("sqlite"):
    @event.listens_for(engine, "connect")
    def set_sqlite_pragma(dbapi_connection, connection_record):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

# Session factory for generating database sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """FastAPI dependency that yields an independent database session per request

    and guarantees cleanup by closing the session after the request finishes.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
