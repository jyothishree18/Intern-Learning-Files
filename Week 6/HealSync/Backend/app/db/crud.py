
from sqlalchemy.orm import Session
from app.db.models import Patient


# Create a new patient
def create_patient(db: Session, patient_data: dict):
    patient = Patient(**patient_data)
    db.add(patient)
    db.commit()
    db.refresh(patient)
    return patient


# Get all patients
def get_patients(db: Session):
    return db.query(Patient).all()


# Get patient by ID
def get_patient(db: Session, patient_id: int):
    return (
        db.query(Patient)
        .filter(Patient.id == patient_id)
        .first()
    )


# Check whether patient code already exists
def get_patient_by_code(db: Session, patient_code: str):
    return (
        db.query(Patient)
        .filter(Patient.patient_code == patient_code)
        .first()
    )


# Check whether email already exists
def get_patient_by_email(db: Session, email: str):
    return (
        db.query(Patient)
        .filter(Patient.email == email)
        .first()
    )


# Update patient
def update_patient(
    db: Session,
    patient_id: int,
    patient_data: dict
):
    patient = get_patient(db, patient_id)

    if patient is None:
        return None

    for field, value in patient_data.items():
        setattr(patient, field, value)

    db.commit()
    db.refresh(patient)

    return patient


# Delete patient
def delete_patient(db: Session, patient_id: int):
    patient = get_patient(db, patient_id)

    if patient is None:
        return False

    db.delete(patient)
    db.commit()

    return True
