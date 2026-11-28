def test_doctor_cannot_list_staff(client, set_user):
    set_user({
        "sub": "doctor-user",
        "realm_access": {"roles": ["doctor"]},
    })

    response = client.get("/staff")

    assert response.status_code == 403


def test_admin_can_list_staff(client, set_user):
    set_user({
        "sub": "admin-user",
        "realm_access": {"roles": ["admin"]},
    })

    response = client.get("/staff")

    assert response.status_code == 200
    assert isinstance(response.json(), list)
