from fastapi import FastAPI
from pydantic import BaseModel, Field
from datetime import datetime
from uuid import uuid4, UUID

app = FastAPI(title="WIMP - Watchdog Intelligent Monitoring Platform")

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "wimp-api"}

class Alert(BaseModel):
    service_name: str
    severity: str = "normal"
    message: str
    service_version: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    alert_id: UUID = Field(default_factory=uuid4)

@app.post("/alerts")
def create_alert(alert: Alert):
    return {"status": "alert created", "alert": alert}
