
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from app.db import crud, report_crud
from app.db.database import get_db
from app.core.auth import require_roles

from app.schemas.schemas import (
    PatientCreate,
    PatientResponse,
    PatientUpdate,
)

from app.services.patient_service import (
    register_patient,
    delete_patient_record,
    update_patient_record,
)

from app.exceptions.exceptions import (
    PatientNotFoundException,
)


router = APIRouter(
    prefix="/patients",
    tags=["Patients"]
)


# CREATE PATIENT
@router.post(
    "",
    response_model=PatientResponse,
    status_code=status.HTTP_201_CREATED
)
def create_patient(
    patient_data: PatientCreate,
    db: Session = Depends(get_db),
    user=Depends(require_roles("admin"))
):
    return register_patient(db, patient_data)


# GET ALL PATIENTS
@router.get(
    "",
    response_model=list[PatientResponse]
)
def read_patients(
    db: Session = Depends(get_db),
    user=Depends(require_roles("admin", "doctor", "lab_tech"))
):
    return crud.get_patients(db)


# GET PATIENT BY ID
@router.get(
    "/{patient_id}",
    response_model=PatientResponse
)
def read_patient(
    patient_id: int,
    db: Session = Depends(get_db),
    user=Depends(
        require_roles("admin", "doctor", "lab_tech", "patient")
    )
):
    patient = crud.get_patient(db, patient_id)

    if patient is None:
        raise PatientNotFoundException(
            "Patient does not exist."
        )

    user_roles = (
        user.get("realm_access", {})
        .get("roles", [])
    )

    staff_roles = {"admin", "doctor", "lab_tech"}

    # PATIENTS CAN ACCESS ONLY THEIR OWN RECORDS
    if "patient" in user_roles and not staff_roles.intersection(user_roles):

        linked_patient = report_crud.get_patient_by_keycloak_user_id(
            db,
            user.get("sub")
        )

        if linked_patient is None or linked_patient.id != patient.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You are not allowed to access this patient record."
            )

    return patient


# UPDATE PATIENT
@router.put(
    "/{patient_id}",
    response_model=PatientResponse
)
def edit_patient(
    patient_id: int,
    patient_data: PatientUpdate,
    db: Session = Depends(get_db),
    user=Depends(require_roles("admin"))
):
    updated_patient = update_patient_record(
        db,
        patient_id,
        patient_data.model_dump(exclude_unset=True)
    )

    if updated_patient is None:
        raise PatientNotFoundException(
            "Patient does not exist."
        )

    return updated_patient


# DELETE PATIENT
@router.delete("/{patient_id}")
def remove_patient(
    patient_id: int,
    db: Session = Depends(get_db),
    user=Depends(require_roles("admin"))
):
    deleted = delete_patient_record(
        db,
        patient_id
    )

    if not deleted:
        raise PatientNotFoundException(
            "Patient does not exist."
        )

    return {
        "message": "Patient and Keycloak account deleted successfully."
    }
