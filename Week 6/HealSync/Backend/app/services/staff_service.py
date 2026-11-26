
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.db import staff_crud

from app.core.keycloak_service import (
    create_user_account,
    delete_patient_account,
)

from app.exceptions.exceptions import (
    StaffNotFoundException,
    StaffAlreadyExistsException,
    InvalidStaffRoleException,
)


# CREATE STAFF MEMBER
def create_staff_member(
    db: Session,
    staff_data
):
    # STEP 1: Validate staff role
    if staff_data.role not in {"doctor", "lab_tech"}:
        raise InvalidStaffRoleException(
            "Role must be doctor or lab_tech."
        )

    keycloak_user_id = None

    # STEP 2: Create Keycloak account and save staff
    try:
        keycloak_user_id = create_user_account(
            email=staff_data.email,
            password=staff_data.password,
            full_name=staff_data.full_name,
            role=staff_data.role
        )

        # Never save password in PostgreSQL
        staff_values = staff_data.model_dump(
            exclude={"password"}
        )

        staff_values["keycloak_user_id"] = keycloak_user_id

        return staff_crud.create_staff(
            db,
            staff_values
        )

    except ValueError:
        db.rollback()
        _cleanup_keycloak_user(keycloak_user_id)
        raise

    except IntegrityError:
        db.rollback()
        _cleanup_keycloak_user(keycloak_user_id)

        raise StaffAlreadyExistsException(
            "Staff code or email already exists."
        )

    except Exception as exc:
        db.rollback()
        _cleanup_keycloak_user(keycloak_user_id)

        print(
            "Staff registration error:",
            repr(exc)
        )

        raise


# DELETE STAFF MEMBER
def remove_staff_member(
    db: Session,
    staff_id: int
):
    # STEP 1: Check whether staff exists
    staff = staff_crud.get_staff(
        db,
        staff_id
    )

    if staff is None:
        raise StaffNotFoundException(
            "Staff member not found."
        )

    # STEP 2: Delete Keycloak account and database record
    try:
        delete_patient_account(
            staff.keycloak_user_id
        )

        staff_crud.delete_staff(
            db,
            staff_id
        )

    except Exception as exc:
        db.rollback()

        print(
            "Staff deletion error:",
            repr(exc)
        )

        raise


# KEYCLOAK CLEANUP
def _cleanup_keycloak_user(
    keycloak_user_id
):
    if keycloak_user_id:
        try:
            delete_patient_account(
                keycloak_user_id
            )

        except Exception as cleanup_error:
            print(
                "Keycloak cleanup error:",
                repr(cleanup_error)
            )
