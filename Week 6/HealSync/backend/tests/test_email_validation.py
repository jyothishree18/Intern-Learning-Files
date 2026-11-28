import pytest
from pydantic import ValidationError

from app.schemas.schemas import PatientCreate, PatientUpdate, StaffCreate


def patient_payload(email):
    return {
        "patient_code": "PAT-TEST-01",
        "full_name": "Test Patient",
        "age": 30,
        "gender": "Other",
        "contact_number": "9876543210",
        "email": email,
        "password": "TestPass123",
    }


def staff_payload(email):
    return {
        "staff_code": "STAFF-TEST-01",
        "full_name": "Test Staff",
        "email": email,
        "contact_number": "9876543210",
        "role": "doctor",
        "password": "TestPass123",
    }


@pytest.mark.parametrize("email", ["abc@gmail.com", "abc@healsync.com"])
def test_patient_accepts_valid_email_formats(email):
    assert PatientCreate(**patient_payload(email)).email == email


@pytest.mark.parametrize("email", ["abcgmail.com", "abc@", "not-an-email"])
def test_patient_rejects_invalid_email(email):
    with pytest.raises(ValidationError):
        PatientCreate(**patient_payload(email))


def test_staff_accepts_healsync_email():
    assert StaffCreate(**staff_payload("abc@healsync.com")).email == "abc@healsync.com"


def test_staff_rejects_invalid_email():
    with pytest.raises(ValidationError):
        StaffCreate(**staff_payload("abcgmail.com"))


def test_patient_update_allows_omitted_email():
    update = PatientUpdate(full_name="Updated Name")
    assert update.email is None


def test_patient_update_rejects_invalid_email():
    with pytest.raises(ValidationError):
        PatientUpdate(email="abcgmail.com")
