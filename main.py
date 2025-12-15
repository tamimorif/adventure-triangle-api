from fastapi import FastAPI
from contextlib import asynccontextmanager
from typing import Any
from sqlmodel import Session, select
import bcrypt

from db import engine, create_database
from models import User, Partner, EventRegistration, SystemLog


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_database()
    yield


app = FastAPI(
    title="Adventure Triangle API",
    description="Backend API for Internship Assignment (Platform & CRM)",
    version="1.0.0",
    lifespan=lifespan,
)


@app.get("/")
def root() -> dict[str, str]:
    return {"message": "Adventure Triangle API is running!"}


# ---------------- USERS ----------------
@app.post("/api/users/register")
def register_user(full_name: str, email: str, password: str) -> dict[str, Any]:
    # bcrypt hard limit: 72 bytes
    if len(password.encode("utf-8")) > 72:
        return {"error": "Password too long (bcrypt max is 72 bytes)"}

    with Session(engine) as session:
        existing = session.exec(select(User).where(User.email == email)).first()
        if existing:
            return {"error": "User already exists"}

        pw_hash = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

        user = User(full_name=full_name, email=email, password_hash=pw_hash)
        session.add(user)
        session.commit()
        session.refresh(user)

        return {"id": user.id, "full_name": user.full_name, "email": user.email}


@app.get("/api/users")
def list_users() -> list[dict[str, Any]]:
    with Session(engine) as session:
        users = session.exec(select(User)).all()
        return [
            {
                "id": u.id,
                "full_name": u.full_name,
                "email": u.email,
                "created_at": u.created_at,
            }
            for u in users
        ]


# ---------------- PARTNERS ----------------
@app.post("/api/partners/onboard")
def onboard_partner(company_name: str, contact_email: str, phone: str, description: str) -> dict[str, Any]:
    with Session(engine) as session:
        partner = Partner(
            company_name=company_name,
            contact_email=contact_email,
            phone=phone,
            description=description,
        )
        session.add(partner)
        session.commit()
        session.refresh(partner)

        return {
            "id": partner.id,
            "company_name": partner.company_name,
            "contact_email": partner.contact_email,
        }


@app.get("/api/partners")
def list_partners() -> list[dict[str, Any]]:
    with Session(engine) as session:
        partners = session.exec(select(Partner)).all()
        return [
            {
                "id": p.id,
                "company_name": p.company_name,
                "contact_email": p.contact_email,
                "phone": p.phone,
                "description": p.description,
                "created_at": p.created_at,
            }
            for p in partners
        ]


# ---------------- EVENTS ----------------
@app.post("/api/events/register")
def register_event(event_id: str, attendee_name: str, attendee_email: str) -> dict[str, Any]:
    with Session(engine) as session:
        reg = EventRegistration(
            event_id=event_id,
            attendee_name=attendee_name,
            attendee_email=attendee_email,
        )
        session.add(reg)
        session.commit()
        session.refresh(reg)

        return {
            "id": reg.id,
            "event_id": reg.event_id,
            "attendee_name": reg.attendee_name,
            "attendee_email": reg.attendee_email,
        }


@app.get("/api/events")
def list_events() -> list[dict[str, Any]]:
    with Session(engine) as session:
        events = session.exec(select(EventRegistration)).all()
        return [
            {
                "id": e.id,
                "event_id": e.event_id,
                "attendee_name": e.attendee_name,
                "attendee_email": e.attendee_email,
                "created_at": e.created_at,
            }
            for e in events
        ]


# ---------------- SYSTEM LOGGING ----------------
@app.post("/api/system/log")
def create_log(level: str, message: str) -> dict[str, Any]:
    with Session(engine) as session:
        log = SystemLog(level=level, message=message)
        session.add(log)
        session.commit()
        session.refresh(log)

        return {"id": log.id, "level": log.level, "message": log.message, "timestamp": log.timestamp}


@app.get("/api/system/logs")
def list_logs() -> list[dict[str, Any]]:
    with Session(engine) as session:
        logs = session.exec(select(SystemLog)).all()
        return [
            {"id": l.id, "level": l.level, "message": l.message, "timestamp": l.timestamp}
            for l in logs
        ]
