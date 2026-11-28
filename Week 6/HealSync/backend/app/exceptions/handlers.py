
from fastapi import Request
from fastapi.responses import JSONResponse

from app.exceptions.exceptions import (
    PatientNotFoundException,
    PatientAlreadyExistsException,
    PatientHasReportsException,
    ReportNotFoundException,
    StaffNotFoundException,
    StaffAlreadyExistsException,
    InvalidStaffRoleException,
)


# PATIENT NOT FOUND
async def patient_not_found_handler(
    request: Request,
    exc: PatientNotFoundException
):
    return JSONResponse(
        status_code=404,
        content={"detail": str(exc)}
    )


# PATIENT ALREADY EXISTS
async def patient_exists_handler(
    request: Request,
    exc: PatientAlreadyExistsException
):
    return JSONResponse(
        status_code=409,
        content={"detail": str(exc)}
    )


# PATIENT HAS MEDICAL REPORTS
async def patient_has_reports_handler(
    request: Request,
    exc: PatientHasReportsException
):
    return JSONResponse(
        status_code=409,
        content={"detail": str(exc)}
    )


# REPORT NOT FOUND
async def report_not_found_handler(
    request: Request,
    exc: ReportNotFoundException
):
    return JSONResponse(
        status_code=404,
        content={"detail": str(exc)}
    )


# STAFF NOT FOUND
async def staff_not_found_handler(
    request: Request,
    exc: StaffNotFoundException
):
    return JSONResponse(
        status_code=404,
        content={"detail": str(exc)}
    )


# STAFF ALREADY EXISTS
async def staff_exists_handler(
    request: Request,
    exc: StaffAlreadyExistsException
):
    return JSONResponse(
        status_code=409,
        content={"detail": str(exc)}
    )


# INVALID STAFF ROLE
async def invalid_staff_role_handler(
    request: Request,
    exc: InvalidStaffRoleException
):
    return JSONResponse(
        status_code=400,
        content={"detail": str(exc)}
    )
