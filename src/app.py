"""
High School Management System API

A super simple FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.

Now with persistent database storage using SQLAlchemy and PostgreSQL.
"""

from fastapi import FastAPI, HTTPException, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
import os
from pathlib import Path

from database import (
    Activity, Participant, get_db, init_db, 
    seed_initial_data, SessionLocal
)

app = FastAPI(title="Mergington High School API",
              description="API for viewing and signing up for extracurricular activities")

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(Path(__file__).parent,
          "static")), name="static")


# Initialize database on startup
@app.on_event("startup")
def startup_event():
    """Initialize database and seed data on application startup"""
    init_db()
    db = SessionLocal()
    try:
        seed_initial_data(db)
    finally:
        db.close()



@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/activities")
def get_activities(db: Session = Depends(get_db)):
    """Retrieve all activities with their participants"""
    activities = db.query(Activity).all()
    
    # Transform to match original format
    result = {}
    for activity in activities:
        result[activity.name] = {
            "description": activity.description,
            "schedule": activity.schedule,
            "max_participants": activity.max_participants,
            "participants": [p.email for p in activity.participants]
        }
    
    return result


@app.post("/activities/{activity_name}/signup")
def signup_for_activity(
    activity_name: str,
    email: str,
    db: Session = Depends(get_db)
):
    """Sign up a student for an activity"""
    # Get the activity
    activity = db.query(Activity).filter(
        Activity.name == activity_name
    ).first()
    
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Check if student is already signed up
    existing_participant = db.query(Participant).filter(
        Participant.email == email
    ).filter(
        Participant.activities.any(Activity.id == activity.id)
    ).first()
    
    if existing_participant:
        raise HTTPException(
            status_code=400,
            detail="Student is already signed up"
        )

    # Check if activity is full
    if len(activity.participants) >= activity.max_participants:
        raise HTTPException(
            status_code=400,
            detail="Activity is full"
        )

    # Get or create participant
    participant = db.query(Participant).filter(
        Participant.email == email
    ).first()
    
    if not participant:
        participant = Participant(email=email)
        db.add(participant)
        db.flush()  # Get the participant in this session

    # Add student to activity
    activity.participants.append(participant)
    db.commit()
    
    return {"message": f"Signed up {email} for {activity_name}"}


@app.delete("/activities/{activity_name}/unregister")
def unregister_from_activity(
    activity_name: str,
    email: str,
    db: Session = Depends(get_db)
):
    """Unregister a student from an activity"""
    # Get the activity
    activity = db.query(Activity).filter(
        Activity.name == activity_name
    ).first()
    
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Get the participant
    participant = db.query(Participant).filter(
        Participant.email == email
    ).first()
    
    if not participant:
        raise HTTPException(
            status_code=400,
            detail="Student is not signed up for this activity"
        )

    # Check if student is signed up for this activity
    if activity not in participant.activities:
        raise HTTPException(
            status_code=400,
            detail="Student is not signed up for this activity"
        )

    # Remove student from activity
    participant.activities.remove(activity)
    db.commit()
    
    return {"message": f"Unregistered {email} from {activity_name}"}
