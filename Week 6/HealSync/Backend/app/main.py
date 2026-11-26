
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from sqlalchemy import text

from app.routes.report_routes import router as report_router
from app.routes.patient_routes import router as patient_router
from app.routes.staff_routes import router as staff_router

from app.db import models
from app.db.database import Base, engine

from app.exceptions.exceptions import (
    PatientNotFoundException,
    PatientAlreadyExistsException,
    ReportNotFoundException,
    StaffNotFoundException,
    StaffAlreadyExistsException,
    InvalidStaffRoleException,
)

from app.exceptions.handlers import (
    patient_not_found_handler,
    patient_exists_handler,
    report_not_found_handler,
    staff_not_found_handler,
    staff_exists_handler,
    invalid_staff_role_handler,
)


# APPLICATION LIFESPAN
@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


# FASTAPI APPLICATION
app = FastAPI(
    title="HealSync API",
    description="Hospital Medical Report Management System",
    version="1.0.0",
    lifespan=lifespan
)


# CENTRALIZED EXCEPTION HANDLERS

app.add_exception_handler(
    PatientNotFoundException,
    patient_not_found_handler
)

app.add_exception_handler(
    PatientAlreadyExistsException,
    patient_exists_handler
)

app.add_exception_handler(
    ReportNotFoundException,
    report_not_found_handler
)

app.add_exception_handler(
    StaffNotFoundException,
    staff_not_found_handler
)

app.add_exception_handler(
    StaffAlreadyExistsException,
    staff_exists_handler
)

app.add_exception_handler(
    InvalidStaffRoleException,
    invalid_staff_role_handler
)


# CORS CONFIGURATION
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


# REGISTER API ROUTERS
app.include_router(patient_router)
app.include_router(report_router)
app.include_router(staff_router)


# HOME ENDPOINT
@app.get("/")
def home():
    return {
        "message": "Welcome to HealSync!",
        "status": "API is running"
    }


# HEALTH CHECK
@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }


# DATABASE HEALTH CHECK
@app.get("/db-health")
def database_health():
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))

    return {
        "database": "connected"
    }
