# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import models, routes
from .database import engine

# Create database tables
models.Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(title="Construction AI Task Manager")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(routes.router, tags=["projects"])

# Root endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to Construction AI Task Manager"}
