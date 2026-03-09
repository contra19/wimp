from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import and_
from database import get_db, Alert, Base, engine
from pydantic import BaseModel, Field
from datetime import datetime, timedelta
from uuid import uuid4, UUID
from enum import Enum
import math

# Create tables on startup
Base.metadata.create_all(bind=engine)

app = FastAPI(title="WIMP - Watchdog Intelligent Monitoring Platform")

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "wimp-api"}

class SeverityLevel(str, Enum):
    info = "info"
    normal = "normal"
    warning = "warning"
    critical = "critical"

class AlertCreate(BaseModel):
    service_name: str
    severity: SeverityLevel = SeverityLevel.normal
    message: str
    service_version: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    alert_id: UUID = Field(default_factory=uuid4)
    is_duplicate: bool = False

class AlertResponse(BaseModel):
    service_name: str
    severity: SeverityLevel
    message: str
    service_version: str
    timestamp: datetime
    is_duplicate: bool

    class Config:
        from_attributes = True

class AlertListResponse(BaseModel):
    total: int
    page: int
    size: int
    total_pages: int
    alerts: list[AlertResponse]

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

@app.get("/alerts", response_model=AlertListResponse)
def get_alerts(db: Session = Depends(get_db), severity: SeverityLevel=None, service_name: str=None, start_date: datetime=None,
               end_date: datetime=None, page: int = 1, page_size: int=10,):
    fifteen_minutes_ago = datetime.utcnow() - timedelta(minutes=15)

    if (start_date and not end_date) or (end_date and not start_date):
        raise HTTPException(status_code=400, detail="Both start_date and end_date are required together")
    if start_date and end_date and start_date > end_date:
        raise HTTPException(status_code=400, detail="start_date cannot be greater than end_date")
    if start_date and end_date:
        query = db.query(Alert).filter(and_(Alert.timestamp >= start_date, Alert.timestamp <= end_date))
    else:
        query = db.query(Alert).filter(Alert.timestamp >= fifteen_minutes_ago)
    if severity:
        query = query.filter(Alert.severity == severity)
    if service_name:
        query = query.filter(Alert.service_name == service_name)    

    alert_totals = query.count()
    total_pages = math.ceil(alert_totals / page_size)
    offset = (page - 1) * page_size
    alerts = query.order_by(Alert.timestamp.desc()).offset(offset).limit(page_size).all()
    return AlertListResponse(total=alert_totals,
                             page=page,
                             size=page_size,
                             total_pages=total_pages,
                             alerts=alerts)
