
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.db import crud
from app.core.keycloak_service import (
    create_patient_account,
    delete_patient_account,
)
from app.exceptions.exceptions import (
    PatientAlreadyExistsException,
)


def register_patient(db: Session, patient_data):
    # Check duplicate patient code
    existing_patient = crud.get_patient_by_code(
        db,
        patient_data.patient_code
    )

    if existing_patient:
        raise PatientAlreadyExistsException(
            "Patient code already exists."
        )

    # Check duplicate email
    if patient_data.email:
        existing_email = crud.get_patient_by_email(
            db,
            patient_data.email
        )

        if existing_email:
            raise PatientAlreadyExistsException(
                "Patient email already exists."
            )

    keycloak_user_id = None

    try:
        # Create Keycloak account
        keycloak_user_id = create_patient_account(
            email=patient_data.email,
            password=patient_data.password,
            full_name=patient_data.full_name
        )

        # Exclude password before saving
        patient_values = patient_data.model_dump(
            exclude={"password"}
        )

        patient_values["keycloak_user_id"] = keycloak_user_id

        return crud.create_patient(
            db,
            patient_values
        )

    except ValueError as exc:
        db.rollback()
        _cleanup_keycloak_user(keycloak_user_id)

        raise PatientAlreadyExistsException(str(exc))

    except IntegrityError:
        db.rollback()
        _cleanup_keycloak_user(keycloak_user_id)

        raise PatientAlreadyExistsException(
            "Patient code or email already exists."
        )

    except Exception as exc:
        db.rollback()
        _cleanup_keycloak_user(keycloak_user_id)

        print("Patient registration error:", repr(exc))
        raise


def _cleanup_keycloak_user(keycloak_user_id):
    if keycloak_user_id:
        try:
            delete_patient_account(keycloak_user_id)
        except Exception as cleanup_error:
            print(
                "Keycloak cleanup error:",
                repr(cleanup_error)
            )
