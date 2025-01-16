from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# The URL of the database. For SQLite, it uses a relative path to the `test.db` file.
DATABASE_URL = "sqlite:///./test.db"  # Replace with your DB URL for production.

# Create an engine that will interact with the database.
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# SessionLocal is a factory for creating new session instances, which interact with the database.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for the declarative model. All models will inherit from this base to define their structure.
Base = declarative_base()

def get_db():
    """
    Dependency that provides a database session to the route handler.
    
    This function uses the `SessionLocal` sessionmaker to create a new session instance
    which is used in route handlers for database interactions. After the request is processed,
    the session is closed.

    Yields:
        db: The session instance that can be used for database queries and commits.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
