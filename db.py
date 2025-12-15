from sqlmodel import SQLModel, create_engine

# Simple local DB for assignment/demo
DATABASE_URL = "sqlite:///database.db"

engine = create_engine(DATABASE_URL, echo=False)

def create_database():
    """Create database tables if they don't exist."""
    SQLModel.metadata.create_all(engine)
