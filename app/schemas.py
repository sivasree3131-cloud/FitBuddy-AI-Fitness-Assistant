from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

# User Input Validation Schema
class UserCreate(BaseModel):
    name: str = Field(..., min_length=2, example="Sivasree")
    age: int = Field(..., gt=0, lt=120, example=18)
    weight: float = Field(..., gt=0, example=55.0)
    goal: str = Field(..., example="Weight Loss")
    intensity: str = Field(..., example="Medium")

# Feedback Request Schema
class FeedbackRequest(BaseModel):
    workout_id: int
    user_feedback: str

# Response Schemas
class WorkoutResponse(BaseModel):
    id: int
    user_id: int
    plan_content: str
    nutrition_tip: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True
class FeedbackCreate(BaseModel):
    user_id: int
    rating: int
    comment: str | None = None
    