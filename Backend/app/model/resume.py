from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Float, JSON
from sqlalchemy.sql import func
from app.database.database import Base

class ResumeAnalysis(Base):
    __tablename__ = "resume_analysis"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))

    filename = Column(String(255))
    extracted_text = Column(String)

    key_skills = Column(JSON)          # stored as comma-separated or JSON
    ats_score = Column(Integer)
    recommendations = Column(JSON)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
