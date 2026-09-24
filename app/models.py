from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    weight = Column(Integer, nullable=False)
    goal = Column(String, nullable=False)
    intensity = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    workouts = relationship("WorkoutPlan", back_populates="user")

class WorkoutPlan(Base):
    __tablename__ = "workout_plans"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    plan_content = Column(Text, nullable=False)
    nutrition_tip = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="workouts")
    feedbacks = relationship("Feedback", back_populates="workout_plan")

class Feedback(Base):
    __tablename__ = "feedbacks"

    id = Column(Integer, primary_key=True, index=True)
    workout_id = Column(Integer, ForeignKey("workout_plans.id"))
    user_feedback = Column(Text, nullable=False)
    updated_plan_content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    workout_plan = relationship("WorkoutPlan", back_populates="feedbacks")