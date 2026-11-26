
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db import crud
from app.db.database import get_db
from app.core.auth import require_roles

from app.schemas.schemas import (
    PatientCreate,
    PatientResponse,
    PatientUpdate,
)

from app.services.patient_service import register_patient

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
    updated_patient = crud.update_patient(
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
    deleted = crud.delete_patient(db, patient_id)

    if not deleted:
        raise PatientNotFoundException(
            "Patient does not exist."
        )

    return {
        "message": "Patient deleted successfully."
    }
