# FitBuddy – AI Fitness Assistant

FitBuddy is a simple AI-powered fitness assistant that creates personalized workout plans and nutrition tips based on a user's fitness goals.

## About the Project

I built FitBuddy as a Generative AI project to explore how AI can be used to create personalized fitness guidance.
Users can enter basic details such as their name, age, weight, fitness goal, and workout intensity. FitBuddy then uses Google Gemini to generate a customized workout plan and nutrition tips.

## Features

- Personalized workout plan generation
- AI-generated nutrition tips
- Different fitness goals and workout intensities
- Simple and user-friendly interface
- FastAPI backend
- SQLite database for storing user and workout data
- Google Gemini AI integration

## Technologies Used

- Python
- FastAPI
- Google Gemini AI
- SQLite
- SQLAlchemy
- HTML
- CSS
- JavaScript

## Project Structure

FitBuddy/
│
├── app/
│   ├── __init__.py
│   ├── ai_service.py
│   ├── database.py
│   ├── main.py
│   ├── models.py
│   └── schemas.py
│
├── static/
│   ├── index.html
│   ├── script.js
│   └── style.css
│
├── .gitignore
└── requirements.txt
