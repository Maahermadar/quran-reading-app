from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Date, Enum, Float, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import enum
from datetime import datetime

Base = declarative_base()

class GoalStatus(str, enum.Enum):
    active = "active"
    completed = "completed"
    cancelled = "cancelled"

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True, index=True)
    password_hash = Column(String)
    avatar_url = Column(String, nullable=True)
    lifetime_completions = Column(Integer, default=0)
    is_cycle_completed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    logs = relationship("ReadingLog", back_populates="user")
    goals = relationship("Goal", back_populates="user")
    stats = relationship("LifetimeStat", back_populates="user", uselist=False)

class ReadingLog(Base):
    __tablename__ = "reading_logs"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    start_page = Column(Integer)
    end_page = Column(Integer)
    completion_counted = Column(Integer, default=0)  # Guard: 1 if this log already triggered a completion increment
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="logs")

class Goal(Base):
    __tablename__ = "goals"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    start_at = Column(DateTime, default=datetime.utcnow)
    target_pages = Column(Integer)
    target_days = Column(Integer)
    status = Column(Enum(GoalStatus), default=GoalStatus.active)

    user = relationship("User", back_populates="goals")

class LifetimeStat(Base):
    __tablename__ = "lifetime_stats"
    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    total_completions = Column(Integer, default=0)
    is_cycle_completed = Column(Boolean, default=False)

    user = relationship("User", back_populates="stats")
