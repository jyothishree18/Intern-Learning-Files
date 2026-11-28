
from sqlalchemy.orm import Session

from app.db.models import Patient

from app.exceptions.exceptions import (
    PatientAlreadyExistsException,
    PatientHasReportsException,
)


# CREATE PATIENT
def create_patient(db: Session, patient_data: dict):
    patient = Patient(**patient_data)

    db.add(patient)
    db.commit()
    db.refresh(patient)

    return patient


# GET ALL PATIENTS
def get_patients(db: Session):
    return db.query(Patient).all()


# GET PATIENT BY ID
def get_patient(db: Session, patient_id: int):
    return (
        db.query(Patient)
        .filter(Patient.id == patient_id)
        .first()
    )


# CHECK WHETHER PATIENT CODE ALREADY EXISTS
def get_patient_by_code(db: Session, patient_code: str):
    return (
        db.query(Patient)
        .filter(Patient.patient_code == patient_code)
        .first()
    )


# CHECK WHETHER EMAIL ALREADY EXISTS
def get_patient_by_email(db: Session, email: str):
    return (
        db.query(Patient)
        .filter(Patient.email == email)
        .first()
    )


# UPDATE PATIENT
def update_patient(
    db: Session,
    patient_id: int,
    patient_data: dict
):
    patient = get_patient(db, patient_id)

    if patient is None:
        return None

    # CHECK DUPLICATE PATIENT CODE
    if patient_data.get("patient_code"):
        existing_code = get_patient_by_code(
            db,
            patient_data["patient_code"]
        )

        if existing_code and existing_code.id != patient_id:
            raise PatientAlreadyExistsException(
                "Patient code already exists."
            )

    # CHECK DUPLICATE EMAIL
    if patient_data.get("email"):
        existing_email = get_patient_by_email(
            db,
            patient_data["email"]
        )

        if existing_email and existing_email.id != patient_id:
            raise PatientAlreadyExistsException(
                "Patient email already exists."
            )

    # UPDATE PATIENT FIELDS
    for field, value in patient_data.items():
        setattr(patient, field, value)

    db.commit()
    db.refresh(patient)

    return patient



# DELETE PATIENT
def delete_patient(db: Session, patient_id: int):
    patient = get_patient(db, patient_id)

    if patient is None:
        return False

    # CHECK WHETHER PATIENT HAS MEDICAL REPORTS
    from app.db import report_crud

    existing_reports = report_crud.get_patient_reports(
        db,
        patient_id
    )

    if existing_reports:
        raise PatientHasReportsException(
            "Cannot delete patient because medical reports exist."
        )

    # DELETE PATIENT WITHOUT COMMITTING
    db.delete(patient)
    db.flush()

    return patient

