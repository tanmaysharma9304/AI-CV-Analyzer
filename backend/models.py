from datetime import datetime
from sqlalchemy import String, Text, Float, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    resumes: Mapped[list["Resume"]] = relationship(back_populates="user")

class Resume(Base):
    __tablename__ = "resumes"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=True)
    filename: Mapped[str] = mapped_column(String(255))
    stored_path: Mapped[str] = mapped_column(String(500))
    raw_text: Mapped[str] = mapped_column(Text)
    parsed_json: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    # The database foreign key remains nullable; avoid PEP 604 unions here because
    # SQLAlchemy 2.0.36 cannot resolve them under Python 3.14 during mapper setup.
    user: Mapped["User"] = relationship(back_populates="resumes")
    score: Mapped["Score"] = relationship(back_populates="resume", uselist=False)
    reports: Mapped[list["Report"]] = relationship(back_populates="resume")

class Score(Base):
    __tablename__ = "scores"
    id: Mapped[int] = mapped_column(primary_key=True)
    resume_id: Mapped[int] = mapped_column(ForeignKey("resumes.id"), unique=True)
    overall: Mapped[float] = mapped_column(Float)
    ats: Mapped[float] = mapped_column(Float)
    skill: Mapped[float] = mapped_column(Float)
    project: Mapped[float] = mapped_column(Float)
    experience: Mapped[float] = mapped_column(Float)
    breakdown_json: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    resume: Mapped[Resume] = relationship(back_populates="score")

class Report(Base):
    __tablename__ = "reports"
    id: Mapped[int] = mapped_column(primary_key=True)
    resume_id: Mapped[int] = mapped_column(ForeignKey("resumes.id"))
    path: Mapped[str] = mapped_column(String(500))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    resume: Mapped[Resume] = relationship(back_populates="reports")
