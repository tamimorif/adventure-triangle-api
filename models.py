from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime, timezone

def utc_now() -> datetime:
    """Timezone-aware UTC time (avoids datetime.utcnow deprecation warnings)."""
    return datetime.now(timezone.utc)

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    email: str
    password: str
    created_at: datetime = Field(default_factory=utc_now)

class Partner(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    company_name: str
    contact_email: str
    created_at: datetime = Field(default_factory=utc_now)

class EventRegistration(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    event_name: str
    attendee_email: str
    created_at: datetime = Field(default_factory=utc_now)

class Log(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    source: str
    message: str
    created_at: datetime = Field(default_factory=utc_now)
