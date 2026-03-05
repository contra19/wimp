from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import get_db, Alert, Base, engine
from pydantic import BaseModel, Field
from datetime import datetime
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

@app.post("/alerts")
def create_alert(alert: AlertCreate, db: Session = Depends(get_db)):
    db.add(Alert(**alert.dict()))
    db.commit()
    return {"status": "alert created", "alert": alert}
