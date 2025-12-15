from fastapi import FastAPI
from contextlib import asynccontextmanager
from sqlmodel import Session, select
from passlib.hash import bcrypt

from db import engine, create_database
from models import User, Partner, EventRegistration, Log

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create DB tables once when app starts
    create_database()
    yield

app = FastAPI(title="Adventure Triangle API (Intern Backend)", lifespan=lifespan)

@app.get("/")
def health_check():
    return {"status": "Backend is running"}

# ---------------- USERS ----------------
@app.post("/users/register")
def register_user(name: str, email: str, password: str):
    with Session(engine) as session:
        existing_user = session.exec(
            select(User).where(User.email == email)
        ).first()

        if existing_user:
            return {"error": "User already exists"}

        user = User(
            name=name,
            email=email,
            password=bcrypt.hash(password)
        )

        session.add(user)
        session.commit()
        session.refresh(user)

        return {
            "id": user.id,
            "name": user.name,
            "email": user.email
        }

@app.get("/users")
def get_users():
    with Session(engine) as session:
        users = session.exec(select(User)).all()
        # Hide password hashes in the response (simple safety)
        return [{"id": u.id, "name": u.name, "email": u.email, "created_at": u.created_at} for u in users]

# ---------------- PARTNERS ----------------
@app.post("/partners/register")
def register_partner(company_name: str, contact_email: str):
    with Session(engine) as session:
        partner = Partner(company_name=company_name, contact_email=contact_email)
        session.add(partner)
        session.commit()
        session.refresh(partner)

        return {
            "id": partner.id,
            "company_name": partner.company_name,
            "contact_email": partner.contact_email
        }

@app.get("/partners")
def get_partners():
    with Session(engine) as session:
        partners = session.exec(select(Partner)).all()
        return partners

# ---------------- EVENTS ----------------
@app.post("/events/register")
def register_event(event_name: str, attendee_email: str):
    with Session(engine) as session:
        event = EventRegistration(event_name=event_name, attendee_email=attendee_email)
        session.add(event)
        session.commit()
        session.refresh(event)

        return {
            "id": event.id,
            "event_name": event.event_name,
            "attendee_email": event.attendee_email
        }

@app.get("/events")
def get_events():
    with Session(engine) as session:
        events = session.exec(select(EventRegistration)).all()
        return events

# ---------------- LOGGING ----------------
@app.post("/logs")
def log_message(source: str, message: str):
    with Session(engine) as session:
        log = Log(source=source, message=message)
        session.add(log)
        session.commit()
        session.refresh(log)

        return {
            "id": log.id,
            "source": log.source,
            "message": log.message,
            "created_at": log.created_at
        }

@app.get("/logs")
def get_logs():
    with Session(engine) as session:
        logs = session.exec(select(Log)).all()
        return logs
