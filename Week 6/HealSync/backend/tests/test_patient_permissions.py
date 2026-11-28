from app.db.models import Patient


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


def patient_user(subject):
    return {
        "sub": subject,
        "realm_access": {"roles": ["patient"]},
    }


def test_patient_can_read_own_record(client, db_session, set_user):
    patient = make_patient(db_session, "PAT-OWN", "own@example.com", "patient-1")
    set_user(patient_user("patient-1"))

    response = client.get(f"/patients/{patient.id}")

    assert response.status_code == 200
    assert response.json()["id"] == patient.id


def test_patient_cannot_read_another_patient_record(client, db_session, set_user):
    patient = make_patient(db_session, "PAT-OTHER", "other@example.com", "patient-2")
    set_user(patient_user("patient-1"))

    response = client.get(f"/patients/{patient.id}")

    assert response.status_code == 403


def test_doctor_can_read_patient_record(client, db_session, set_user):
    patient = make_patient(db_session, "PAT-DOCTOR", "doctor-view@example.com", "patient-3")
    set_user({
        "sub": "doctor-user",
        "realm_access": {"roles": ["doctor"]},
    })

    response = client.get(f"/patients/{patient.id}")

    assert response.status_code == 200


def test_patient_cannot_list_all_patients(client, set_user):
    set_user(patient_user("patient-1"))

    response = client.get("/patients")

    assert response.status_code == 403
