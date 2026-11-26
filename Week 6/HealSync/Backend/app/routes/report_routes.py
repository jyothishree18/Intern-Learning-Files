
import uuid
from datetime import date
from pathlib import Path

from fastapi import (
    APIRouter,
    Depends,
    File,
    Form,
    HTTPException,
    UploadFile,
    status,
)
from sqlalchemy.orm import Session

from app.db import report_crud
from app.core.auth import require_roles
from app.db.database import get_db
from app.db.models import Patient
from app.schemas.schemas import ReportResponse

from app.services.report_service import (
    create_report_record,
    get_report_presigned_url,
    delete_report_record,
)

from app.exceptions.exceptions import (
    ReportNotFoundException,
)


router = APIRouter(
    prefix="/reports",
    tags=["Reports"],
)


ALLOWED_TYPES = {
    "application/pdf",
    "image/jpeg",
    "image/png",
}

MAX_FILE_SIZE = 10 * 1024 * 1024

STAFF_ROLES = {"admin", "doctor", "lab_tech"}


# GET LINKED PATIENT
def get_linked_patient(db: Session, user: dict):
    keycloak_user_id = user.get("sub")

    if not keycloak_user_id:
        raise HTTPException(
            status_code=401,
            detail="User ID not found in access token.",
        )

    patient = report_crud.get_patient_by_keycloak_user_id(
        db,
        keycloak_user_id,
    )

    if patient is None:
        raise HTTPException(
            status_code=403,
            detail="No patient record is linked to this account.",
        )

    return patient


# UPLOAD REPORT
@router.post(
    "/upload",
    response_model=ReportResponse,
    status_code=status.HTTP_201_CREATED,
)
def upload_report(
    report_code: str = Form(...),
    patient_id: int = Form(...),
    report_type: str = Form(...),
    report_date: date = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    user=Depends(require_roles("admin", "doctor", "lab_tech")),
):
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(
            status_code=400,
            detail="Only PDF, JPEG and PNG files are allowed.",
        )

    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="Filename is required.",
        )

    file_content = file.file.read(MAX_FILE_SIZE + 1)

    if len(file_content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=413,
            detail="File size must not exceed 10 MB.",
        )

    file.file.seek(0)

    patient = db.query(Patient).filter(
        Patient.id == patient_id
    ).first()

    if patient is None:
        raise HTTPException(
            status_code=404,
            detail="Patient not found.",
        )

    safe_filename = Path(file.filename).name
    storage_key = f"reports/{uuid.uuid4()}_{safe_filename}"

    report_data = {
        "report_code": report_code,
        "patient_id": patient_id,
        "report_type": report_type,
        "report_date": report_date,
        "file_name": safe_filename,
        "storage_key": storage_key,
        "content_type": file.content_type,
        "file_size": len(file_content),
        "uploaded_by": user.get(
            "preferred_username",
            user.get("sub", "unknown"),
        ),
    }

    try:
        return create_report_record(
            db,
            report_data,
            file.file,
            storage_key,
            file.content_type,
        )

    except Exception as exc:
        print("Report upload error:", repr(exc))

        raise HTTPException(
            status_code=500,
            detail="Report upload failed.",
        )


# LIST REPORTS
@router.get(
    "",
    response_model=list[ReportResponse],
)
def list_reports(
    db: Session = Depends(get_db),
    user=Depends(
        require_roles("admin", "doctor", "lab_tech", "patient")
    ),
):
    user_roles = set(
        user.get("realm_access", {}).get("roles", [])
    )

    if user_roles.intersection(STAFF_ROLES):
        return report_crud.get_reports(db)

    if "patient" in user_roles:
        patient = get_linked_patient(db, user)

        return report_crud.get_patient_reports(
            db,
            patient.id,
        )

    raise HTTPException(
        status_code=403,
        detail="You do not have permission to view reports.",
    )


# DOWNLOAD REPORT USING PRESIGNED URL
@router.get("/{report_id}/download")
def download_report(
    report_id: int,
    db: Session = Depends(get_db),
    user=Depends(
        require_roles("admin", "doctor", "lab_tech", "patient")
    ),
):
    report = report_crud.get_report(db, report_id)

    if report is None:
        raise ReportNotFoundException(
            "Report not found."
        )

    user_roles = set(
        user.get("realm_access", {}).get("roles", [])
    )

    # Check patient ownership
    if not user_roles.intersection(STAFF_ROLES):
        if "patient" not in user_roles:
            raise HTTPException(
                status_code=403,
                detail="You do not have permission to download reports.",
            )

        patient = get_linked_patient(db, user)

        if report.patient_id != patient.id:
            raise ReportNotFoundException(
                "Report not found."
            )

    try:
        download_url = get_report_presigned_url(
            report.storage_key
        )

        return {
            "message": "Presigned URL generated successfully.",
            "download_url": download_url,
            "expires_in_seconds": 300,
        }

    except Exception as exc:
        print("Presigned URL generation error:", repr(exc))

        raise HTTPException(
            status_code=500,
            detail="Unable to generate download URL.",
        )


# DELETE REPORT
@router.delete(
    "/{report_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def remove_report(
    report_id: int,
    db: Session = Depends(get_db),
    user=Depends(require_roles("admin")),
):
    report = report_crud.get_report(db, report_id)

    if report is None:
        raise ReportNotFoundException(
            "Report not found."
        )

    try:
        delete_report_record(db, report)

    except Exception as exc:
        db.rollback()
        print("Report deletion error:", repr(exc))

        raise HTTPException(
            status_code=500,
            detail="Unable to delete report.",
        )

    return None
