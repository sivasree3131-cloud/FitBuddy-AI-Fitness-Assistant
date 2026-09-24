from fastapi import FastAPI, Depends, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.database import engine, Base, get_db
from app.models import User, WorkoutPlan, Feedback
from app import schemas, ai_service


Base.metadata.create_all(bind=engine)


app = FastAPI(title="FitBuddy - AI Fitness Assistant")


# Static files
app.mount("/static", StaticFiles(directory="static"), name="static")


# --------------------------------------------------
# Home Page
# --------------------------------------------------

@app.get("/")
def read_root():
    return FileResponse("static/index.html")


# --------------------------------------------------
# Generate Workout Plan
# --------------------------------------------------

@app.post("/generate-workout", response_model=schemas.WorkoutResponse)
def create_workout(
    user_data: schemas.UserCreate,
    db: Session = Depends(get_db)
):

    db_user = User(
        name=user_data.name,
        age=user_data.age,
        weight=user_data.weight,
        goal=user_data.goal,
        intensity=user_data.intensity
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    workout_content = ai_service.generate_workout_plan(
        name=db_user.name,
        age=db_user.age,
        weight=db_user.weight,
        goal=db_user.goal,
        intensity=db_user.intensity
    )

    nutrition_tip = ai_service.generate_nutrition_tip(
        goal=db_user.goal
    )

    db_plan = WorkoutPlan(
        user_id=db_user.id,
        plan_content=workout_content,
        nutrition_tip=nutrition_tip
    )

    db.add(db_plan)
    db.commit()
    db.refresh(db_plan)

    return db_plan


# --------------------------------------------------
# Submit Feedback
# --------------------------------------------------

@app.post("/feedback")
def submit_feedback(
    feedback_data: schemas.FeedbackCreate,
    db: Session = Depends(get_db)
):

    user = db.query(User).filter(
        User.id == feedback_data.user_id
    ).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    feedback = Feedback(
        user_id=feedback_data.user_id,
        rating=feedback_data.rating,
        comment=feedback_data.comment
    )

    db.add(feedback)
    db.commit()
    db.refresh(feedback)

    return {
        "message": "Feedback submitted successfully!",
        "feedback_id": feedback.id
    }