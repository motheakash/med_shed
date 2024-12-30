from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
from core.database import async_client, db
from apps.doctors.routes import router as doctor_router
from core.config import settings

# Create FastAPI instance
app = FastAPI(
    title="Doctor Management API",
    description="API for managing doctor registrations and related operations",
    version="1.0.0",
)

# Middleware for CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update with specific domains in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the routes
app.include_router(doctor_router, prefix="/api/v1/doctors", tags=["Doctors"])

# MongoDB Client Setup

@app.on_event("startup")
async def startup_db_client():
    """
    Initialize the database client on app startup.
    """
    app.mongodb_client = async_client
    app.mongodb = db


@app.on_event("shutdown")
async def shutdown_db_client():
    """
    Close the database client on app shutdown.
    """
    app.mongodb_client.close()  # Close the async MongoDB client



@app.get("/", tags=["Health Check"])
async def health_check():
    """
    Health check endpoint to verify the API is running.
    """
    return {"status": "ok", "message": "Doctor Management API is running"}
