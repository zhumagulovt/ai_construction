# Construction AI Task Manager

A FastAPI-based microservice that simulates an AI-powered construction task manager. This service uses Gemini Pro API to generate construction tasks for projects and provides API endpoints to create and manage these projects.

## Features

- Create construction projects with AI-generated tasks
- Retrieve project details and task status
- Background task simulation for task completion
- SQLite database for data storage

## Tech Stack

- FastAPI: Modern, fast web framework for building APIs
- SQLAlchemy: SQL toolkit and ORM
- Gemini Pro API: AI model for generating construction tasks
- SQLite: Lightweight database
- Pydantic: Data validation and settings management
- Uvicorn: ASGI server

## Setup and Installation

### Prerequisites

- Python 3.8+
- pip (Python package installer)

### Installation Steps

   ```bash
   git clone https://github.com/zhumagulovt/ai_construction.git
   cd construction_ai
   pip install -r requirements.txt
```

Create file `.env` and set to variable GEMINI_API_KEY your api key
