
from sqlalchemy.orm import Session

from app.db.models import Patient, Report


# ==========================================
# CREATE REPORT
# ==========================================

def create_report(db: Session, report_data: dict):
    report = Report(**report_data)

    db.add(report)
    db.commit()
    db.refresh(report)

    return report


# ==========================================
# GET REPORT BY CODE
# ==========================================

def get_report_by_code(db: Session, report_code: str):
    return db.query(Report).filter(
        Report.report_code == report_code
    ).first()


# ==========================================
# GET ALL REPORTS
# ==========================================

def get_reports(db: Session):
    results = (
        db.query(Report, Patient.full_name)
        .join(Patient, Report.patient_id == Patient.id)
        .order_by(Report.created_at.desc())
        .all()
    )

    reports = []

    for report, patient_name in results:
        report_data = {
            column.name: getattr(report, column.name)
            for column in Report.__table__.columns
        }

        report_data["patient_name"] = patient_name
        reports.append(report_data)

    return reports


# ==========================================
# GET PATIENT USING KEYCLOAK USER ID
# ==========================================

def get_patient_by_keycloak_user_id(
    db: Session,
    keycloak_user_id: str,
):
    return db.query(Patient).filter(
        Patient.keycloak_user_id == keycloak_user_id
    ).first()


# ==========================================
# GET SINGLE REPORT
# ==========================================

def get_report(db: Session, report_id: int):
    return db.query(Report).filter(
        Report.id == report_id
    ).first()


# ==========================================
# GET REPORTS FOR A SPECIFIC PATIENT
# ==========================================

def get_patient_reports(db: Session, patient_id: int):
    results = (
        db.query(Report, Patient.full_name)
        .join(Patient, Report.patient_id == Patient.id)
        .filter(Report.patient_id == patient_id)
        .order_by(Report.created_at.desc())
        .all()
    )

    reports = []

    for report, patient_name in results:
        report_data = {
            column.name: getattr(report, column.name)
            for column in Report.__table__.columns
        }

        report_data["patient_name"] = patient_name
        reports.append(report_data)

    return reports


# ==========================================
# DELETE REPORT
# ==========================================

def delete_report(db: Session, report: Report):
    db.delete(report)
    db.commit()
