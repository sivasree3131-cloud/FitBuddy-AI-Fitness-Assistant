import os
import time

from dotenv import load_dotenv
from google import genai


# Load environment variables
load_dotenv()

# Get Gemini API key
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError(
        "GEMINI_API_KEY is not set. Please add it to your .env file."
    )

# Create Gemini client
client = genai.Client(api_key=api_key)


def generate_workout_plan(
    name: str,
    age: int,
    goal: str,
    weight: float,
    intensity: str,
):
    """
    Generate a personalized workout plan using Gemini AI.
    """

    prompt = f"""
You are FitBuddy, an AI fitness assistant.

Create a personalized and beginner-friendly workout plan.

User Information:
Name: {name}
Age: {age}
Fitness Goal: {goal}
Weight: {weight} kg
Workout Intensity: {intensity}

Create a practical fitness plan based on this information.

Include:

1. Personalized Introduction
2. Fitness Goal
3. Weekly Workout Plan
4. Exercises
   - Exercise name
   - Sets
   - Repetitions
   - Rest time
5. Warm-up Routine
6. Cool-down Routine
7. Recovery and Sleep Tips
8. Safety Advice

Keep the plan simple, realistic, and suitable for the selected intensity.

Do not recommend extreme dieting or dangerous exercises.
Do not provide medical treatment.
If the user has an injury or medical condition, advise them to
consult a qualified healthcare professional.

Use clear headings and bullet points.
"""

    for attempt in range(3):
        try:
            response = client.models.generate_content(
                model="gemini-3.6-flash",
                contents=prompt,
            )

            if response and response.text:
                return response.text

            raise Exception("Gemini returned an empty response.")

        except Exception as e:
            print(
                f"Gemini workout attempt {attempt + 1}/3 failed: {str(e)}"
            )

            if attempt < 2:
                wait_time = 3 * (attempt + 1)
                print(f"Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
            else:
                return (
                    "Workout plan could not be generated right now. "
                    "Please try again in a few minutes."
                )


def generate_nutrition_tip(goal: str):
    """
    Generate a simple nutrition tip based on the user's fitness goal.
    """

    prompt = f"""
You are FitBuddy, an AI fitness assistant.

The user's fitness goal is:

{goal}

Provide simple and practical nutrition tips suitable for this goal.

Include:

1. Recommended food choices
2. Foods to include regularly
3. Foods to limit
4. Hydration advice
5. One simple daily nutrition tip

Keep the advice general and safe.

Do not provide extreme diets.
Do not provide medical treatment.
Do not recommend starvation or dangerous weight-loss methods.

Use short headings and bullet points.
"""

    for attempt in range(3):
        try:
            response = client.models.generate_content(
                model="gemini-3.6-flash",
                contents=prompt,
            )

            if response and response.text:
                return response.text

            raise Exception("Gemini returned an empty response.")

        except Exception as e:
            print(
                f"Gemini nutrition attempt {attempt + 1}/3 failed: {str(e)}"
            )

            if attempt < 2:
                wait_time = 3 * (attempt + 1)
                print(f"Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
            else:
                return (
                    "Nutrition tips could not be generated right now. "
                    "Please try again in a few minutes."
                )