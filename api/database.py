from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.dialects.postgresql import UUID as pgUUID
from uuid import uuid4
from datetime import datetime
import os
from dotenv import load_dotenv

# load environment variables from .env file at /infra/local/.env
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '../infra/local/.env'))

Base = declarative_base()

DATABASE_URL = f"postgresql://wimp_user:{os.getenv('POSTGRES_PASSWORD')}@localhost:5432/wimp"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Alert(Base):
    __tablename__ = "alerts"

    alert_id = Column(pgUUID(as_uuid=True), primary_key=True,  default=uuid4)
    service_name = Column(String, index=True)
    severity = Column(String, default="normal")
    message = Column(String)
    service_version = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)

def get_db():
    db = SessionLocal()
    try: 
        yield db
    finally: 
        db.close()
