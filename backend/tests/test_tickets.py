
def test_ticket_crud_flow(client, auth_headers):
    create_payload = {
        "title": "Login outage",
        "description": "Users cannot log in.",
        "status": "New",
        "severity": "High",
        "sla_status": "At Risk",
    }
    create_response = client.post("/tickets/", json=create_payload, headers=auth_headers)
    assert create_response.status_code == 201
    created = create_response.json()
    ticket_id = created["id"]
    assert created["title"] == "Login outage"

    list_response = client.get("/tickets/", headers=auth_headers)
    assert list_response.status_code == 200
    assert any(ticket["id"] == ticket_id for ticket in list_response.json())

    detail_response = client.get(f"/tickets/{ticket_id}", headers=auth_headers)
    assert detail_response.status_code == 200
    assert detail_response.json()["notes"] == []

    update_response = client.put(
        f"/tickets/{ticket_id}",
        json={"status": "In Progress", "severity": "Critical"},
        headers=auth_headers,
    )
    assert update_response.status_code == 200
    updated = update_response.json()
    assert updated["status"] == "In Progress"
    assert updated["severity"] == "Critical"

    delete_response = client.delete(f"/tickets/{ticket_id}", headers=auth_headers)
    assert delete_response.status_code == 204

    missing_response = client.get(f"/tickets/{ticket_id}", headers=auth_headers)
    assert missing_response.status_code == 404
    assert missing_response.json()["detail"] == "Ticket not found"
