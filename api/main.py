from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from sqlalchemy import and_
from database import get_db, Alert, Base, engine
from pydantic import BaseModel, Field
from datetime import datetime, timedelta
from uuid import uuid4, UUID

# Create tables on startup
Base.metadata.create_all(bind=engine)

app = FastAPI(title="WIMP - Watchdog Intelligent Monitoring Platform")

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "wimp-api"}

class AlertCreate(BaseModel):
    service_name: str
    severity: str = "normal"
    message: str
    service_version: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    alert_id: UUID = Field(default_factory=uuid4)
    is_duplicate: bool = False

@app.post("/alerts")
def create_alert(alert: AlertCreate, db: Session = Depends(get_db)):
    five_minutes_ago = datetime.utcnow() - timedelta(minutes=5)

    existing_alerts = db.query(Alert).filter(
        and_(
            Alert.service_name == alert.service_name,
            Alert.message == alert.message,
            Alert.timestamp >= five_minutes_ago,
            Alert.is_duplicate == False
        )
    ).first()
    if existing_alerts:
        alert_data = alert.dict()
        alert_data['is_duplicate'] = True
        duplicate = Alert(**alert_data)
        db.add(duplicate)
        db.commit()
        return {"status": "duplicate alert", "message": "An alert for this service has already"
        " been created in the last 5 minutes. Setting the is_duplicate flag to True."}
    

    db.add(Alert(**alert.dict()))
    db.commit()
    return {"status": "alert created", "alert": alert}
