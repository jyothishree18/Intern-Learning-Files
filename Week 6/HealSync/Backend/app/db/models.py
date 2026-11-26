
from datetime import date, datetime

from sqlalchemy import (
    Integer,
    String,
    Date,
    DateTime,
    ForeignKey,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base

class Patient(Base):
    __tablename__ = "patients"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, index=True
    )

    patient_code: Mapped[str] = mapped_column(
        String(20), unique=True, index=True
    )

    full_name: Mapped[str] = mapped_column(String(100))
    age: Mapped[int] = mapped_column(Integer)
    gender: Mapped[str] = mapped_column(String(20))
    contact_number: Mapped[str] = mapped_column(String(20))

    email: Mapped[str | None] = mapped_column(
        String(255), unique=True, nullable=True, index=True
    )

    keycloak_user_id: Mapped[str | None] = mapped_column(
        String(100), unique=True, nullable=True, index=True
    )


class Staff(Base):
    __tablename__ = "staff"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, index=True
    )

    staff_code: Mapped[str] = mapped_column(
        String(20), unique=True, index=True
    )

    full_name: Mapped[str] = mapped_column(String(100))

    email: Mapped[str] = mapped_column(
        String(255), unique=True, nullable=False, index=True
    )

    contact_number: Mapped[str] = mapped_column(String(20))

    role: Mapped[str] = mapped_column(String(20))

    keycloak_user_id: Mapped[str] = mapped_column(
        String(100), unique=True, nullable=False, index=True
    )


class Report(Base):
    __tablename__ = "reports"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, index=True
    )

    report_code: Mapped[str] = mapped_column(
        String(30), unique=True, index=True
    )

    patient_id: Mapped[int] = mapped_column(
        ForeignKey("patients.id"), nullable=False, index=True
    )

    report_type: Mapped[str] = mapped_column(String(100))
    report_date: Mapped[date] = mapped_column(Date)
    file_name: Mapped[str] = mapped_column(String(255))

    storage_key: Mapped[str] = mapped_column(
        String(500), unique=True
    )

    content_type: Mapped[str] = mapped_column(String(100))
    file_size: Mapped[int] = mapped_column(Integer)
    uploaded_by: Mapped[str] = mapped_column(String(100))

    status: Mapped[str] = mapped_column(
        String(30), default="Uploaded"
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
