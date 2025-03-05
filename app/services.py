# app/services.py
import os
import json
import httpx
import asyncio
from typing import List
from dotenv import load_dotenv

load_dotenv()

# Get API key from environment variable or use a default one
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"


async def generate_tasks(project_name: str, location: str) -> List[dict]:
    """
    Generate construction project tasks using Gemini Pro API
    """
    prompt = (
    f"As an AI construction project manager, generate a detailed list of tasks required for building a {project_name} in {location}."
    "Format the response as a JSON array of task objects, each with a 'name' field."
    'Example: [{"name": "Find land"}, {"name": "Get permits"}, {"name": "Hire contractors"}]'
    "Only include the JSON array in your response, no other text."
    )

    # Prepare the request payload
    payload = {
        "contents": [
            {
                "parts": [
                    {
                        "text": prompt
                    }
                ]
            }
        ]
    }

    # Add API key as query parameter
    params = {"key": GEMINI_API_KEY}

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                GEMINI_API_URL,
                json=payload,
                params=params,
                timeout=10,
            )
            response.raise_for_status()

            # Parse the response
            response_data = response.json()

            # Extract the generated text
            generated_text = response_data["candidates"][0]["content"]["parts"][0]["text"]

            # Clean up the text to extract just the JSON array
            generated_text = generated_text.strip()
            if generated_text.startswith("```json"):
                generated_text = generated_text[7:]
            if generated_text.endswith("```"):
                generated_text = generated_text[:-3]

            # Parse the JSON array
            tasks = json.loads(generated_text)

            # Ensure each task has a status field
            for task in tasks:
                task["status"] = "pending"

            return tasks
    except Exception as e:
        raise e
        print(f"Error generating tasks: {e}")
        # Return default tasks if API call fails
        return [
            {"name": "Find land", "status": "pending"},
            {"name": "Get permits", "status": "pending"},
            {"name": "Hire contractors", "status": "pending"},
            {"name": "Develop architectural plans", "status": "pending"},
            {"name": "Secure financing", "status": "pending"}
        ]


# Background task simulation
async def simulate_task_completion(project_id: int, db):
    """
    Simulate task completion for a project
    """
    from .models import Task

    # Wait for a few seconds to simulate work
    await asyncio.sleep(10)

    # Get all pending tasks for the project
    tasks = db.query(Task).filter(Task.project_id == project_id, Task.status == "pending").all()

    if tasks:
        # Mark the first task as completed
        tasks[0].status = "completed"
        db.commit()

        # Update project status to in_progress
        from .models import Project
        project = db.query(Project).filter(Project.id == project_id).first()
        if project and project.status == "processing":
            project.status = "in_progress"
            db.commit()
