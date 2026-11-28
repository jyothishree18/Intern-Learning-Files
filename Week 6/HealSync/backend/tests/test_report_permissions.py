from datetime import date

from app.db.models import Patient, Report


def make_patient(db, code, email, keycloak_user_id):
    patient = Patient(
        patient_code=code,
        full_name=f"Patient {code}",
        age=30,
        gender="Other",
        contact_number="9876543210",
        email=email,
        keycloak_user_id=keycloak_user_id,
    )
    db.add(patient)
    db.commit()
    db.refresh(patient)
    return patient


def make_report(db, patient_id, code):
    report = Report(
        report_code=code,
        patient_id=patient_id,
        report_type="Blood Test",
        report_date=date(2026, 11, 28),
        file_name=f"{code}.pdf",
        storage_key=f"reports/{code}.pdf",
        content_type="application/pdf",
        file_size=1024,
        uploaded_by="test-doctor",
        status="Uploaded",
    )
    db.add(report)
    db.commit()
    db.refresh(report)
    return report


def patient_user(subject):
    return {
        "sub": subject,
        "realm_access": {"roles": ["patient"]},
    }


def test_patient_report_list_contains_only_own_reports(
    client, db_session, set_user
):
    own_patient = make_patient(
        db_session, "PAT-REPORT-OWN", "report-own@example.com", "patient-report-1"
    )
    other_patient = make_patient(
        db_session, "PAT-REPORT-OTHER", "report-other@example.com", "patient-report-2"
    )
    own_report = make_report(db_session, own_patient.id, "REP-OWN")
    make_report(db_session, other_patient.id, "REP-OTHER")

    set_user(patient_user("patient-report-1"))
    response = client.get("/reports")

    assert response.status_code == 200
    report_ids = [item["id"] for item in response.json()]
    assert own_report.id in report_ids
    assert len(report_ids) == 1


def test_patient_cannot_read_another_patients_report(
    client, db_session, set_user
):
    own_patient = make_patient(
        db_session, "PAT-REPORT-SELF", "report-self@example.com", "patient-report-self"
    )
    other_patient = make_patient(
        db_session, "PAT-REPORT-PRIVATE", "report-private@example.com", "patient-report-private"
    )
    make_report(db_session, other_patient.id, "REP-PRIVATE")

    set_user(patient_user("patient-report-self"))
    response = client.get("/reports/1")

    # The route intentionally returns 404 for another patient's report,
    # so it does not disclose whether that report exists.
    assert response.status_code == 404
