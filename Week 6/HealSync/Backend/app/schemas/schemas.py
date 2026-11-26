
from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field


# =========================
# PATIENT SCHEMAS
# =========================

class PatientCreate(BaseModel):
    patient_code: str = Field(min_length=1, max_length=20)
    full_name: str = Field(min_length=1, max_length=100)
    age: int = Field(ge=0, le=130)
    gender: str = Field(min_length=1, max_length=20)
    contact_number: str = Field(min_length=1, max_length=20)
    email: str = Field(min_length=5, max_length=255)
    password: str = Field(min_length=8, max_length=128)


class PatientUpdate(BaseModel):
    full_name: str | None = Field(default=None, min_length=1, max_length=100)
    age: int | None = Field(default=None, ge=0, le=130)
    gender: str | None = Field(default=None, min_length=1, max_length=20)
    contact_number: str | None = Field(default=None, min_length=1, max_length=20)
    email: str | None = Field(default=None, min_length=5, max_length=255)


class PatientResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    patient_code: str
    full_name: str
    age: int
    gender: str
    contact_number: str
    email: str | None = None


# =========================
# REPORT SCHEMAS
# =========================

class ReportResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    patient_name: str | None = None
    report_code: str
    patient_id: int
    report_type: str
    report_date: date
    file_name: str
    content_type: str
    file_size: int
    uploaded_by: str
    status: str
    created_at: datetime



# =========================
# STAFF SCHEMAS
# =========================

class StaffCreate(BaseModel):
    staff_code: str = Field(min_length=1, max_length=20)
    full_name: str = Field(min_length=1, max_length=100)
    email: str = Field(min_length=5, max_length=255)
    contact_number: str = Field(min_length=1, max_length=20)
    role: str
    password: str = Field(min_length=8, max_length=128)


class StaffResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    staff_code: str
    full_name: str
    email: str
    contact_number: str
    role: str
