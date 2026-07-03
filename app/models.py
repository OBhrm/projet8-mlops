
# Décrit la structure de la table "predictions" dans la base de données PostgreSQL via SQLAlchemy

from datetime import datetime

from sqlalchemy import Column, Integer, Float, DateTime, String, Text, JSON
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class Prediction(Base):
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True)

    timestamp = Column(DateTime, default=datetime.utcnow)

    score = Column(Float)

    AMT_INCOME_TOTAL = Column(Float)
    AMT_CREDIT = Column(Float)
    DAYS_BIRTH = Column(Float)
    latency_ms = Column(Float)
    status = Column(String(20))
    error_message = Column(Text)
    input_features = Column(JSON)
