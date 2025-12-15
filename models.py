from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

# NOTE: SQLite is happiest with naive datetimes (no tzinfo).
# We'll store UTC-like timestamps as naive datetime.
def utc_now() -> datetime:
    return datetime.utcnow()

# ---------------- DB TABLES ----------------

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    full_name: str
    email: str = Field(index=True)
    password_hash: str
    created_at: datetime = Field(default_factory=utc_now)

class Partner(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    company_name: str
    contact_email: str
    phone: str
    description: str
    created_at: datetime = Field(default_factory=utc_now)

class EventRegistration(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    event_id: str
    attendee_name: str
    attendee_email: str
    created_at: datetime = Field(default_factory=utc_now)

class SystemLog(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    level: str
    message: str
    timestamp: datetime = Field(default_factory=utc_now)
