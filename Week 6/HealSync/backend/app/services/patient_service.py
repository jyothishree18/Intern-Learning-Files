
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.db import crud

from app.core.keycloak_service import (
    create_patient_account,
    delete_patient_account,
    update_patient_account,
)

from app.exceptions.exceptions import (
    PatientAlreadyExistsException,
)


# REGISTER PATIENT
def register_patient(db: Session, patient_data):

    # CHECK DUPLICATE PATIENT CODE
    existing_patient = crud.get_patient_by_code(
        db,
        patient_data.patient_code
    )

    if existing_patient:
        raise PatientAlreadyExistsException(
            "Patient code already exists."
        )

    # CHECK DUPLICATE EMAIL
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
        # CREATE KEYCLOAK ACCOUNT
        keycloak_user_id = create_patient_account(
            email=patient_data.email,
            password=patient_data.password,
            full_name=patient_data.full_name
        )

        # EXCLUDE PASSWORD BEFORE SAVING
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


# CLEANUP KEYCLOAK ACCOUNT
def _cleanup_keycloak_user(keycloak_user_id):

    if keycloak_user_id:
        try:
            delete_patient_account(keycloak_user_id)

        except Exception as cleanup_error:
            print(
                "Keycloak cleanup error:",
                repr(cleanup_error)
            )


# UPDATE PATIENT AND SYNCHRONIZE KEYCLOAK EMAIL
def update_patient_record(
    db: Session,
    patient_id: int,
    patient_data: dict
):

    patient = crud.get_patient(db, patient_id)

    if patient is None:
        return None

    old_email = patient.email
    new_email = patient_data.get("email")
    keycloak_user_id = patient.keycloak_user_id

    email_changed = (
        new_email is not None
        and new_email != old_email
    )

    # CHECK DUPLICATE EMAIL BEFORE UPDATING KEYCLOAK
    if email_changed:
        existing_email = crud.get_patient_by_email(
            db,
            new_email
        )

        if existing_email and existing_email.id != patient_id:
            raise PatientAlreadyExistsException(
                "Patient email already exists."
            )

    # UPDATE KEYCLOAK ACCOUNT
    if email_changed and keycloak_user_id:
        try:
            update_patient_account(
                keycloak_user_id,
                new_email
            )

        except ValueError as exc:
            raise PatientAlreadyExistsException(str(exc))

    try:
        # UPDATE PATIENT IN POSTGRESQL
        return crud.update_patient(
            db,
            patient_id,
            patient_data
        )

    except Exception:
        db.rollback()

        # RESTORE OLD KEYCLOAK EMAIL IF DATABASE UPDATE FAILS
        if email_changed and keycloak_user_id:
            try:
                update_patient_account(
                    keycloak_user_id,
                    old_email
                )

            except Exception as rollback_error:
                print(
                    "Keycloak email rollback error:",
                    repr(rollback_error)
                )

        raise


# DELETE PATIENT AND KEYCLOAK ACCOUNT
def delete_patient_record(
    db: Session,
    patient_id: int
):

    patient = crud.get_patient(db, patient_id)

    if patient is None:
        return False

    # SAVE KEYCLOAK USER ID BEFORE DATABASE DELETION
    keycloak_user_id = patient.keycloak_user_id

    try:
        # DELETE PATIENT FROM DATABASE TRANSACTION
        deleted_patient = crud.delete_patient(
            db,
            patient_id
        )

        if not deleted_patient:
            db.rollback()
            return False

        # DELETE KEYCLOAK ACCOUNT
        if keycloak_user_id:
            delete_patient_account(keycloak_user_id)

        # COMMIT DATABASE DELETION
        db.commit()

        return True

    except Exception:
        db.rollback()
        raise
