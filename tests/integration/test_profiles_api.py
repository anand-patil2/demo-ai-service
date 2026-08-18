from fastapi import status
from fastapi.testclient import TestClient

from src.api.main import app

client = TestClient(app)


def test_create_and_get_profile():
    payload = {
        "first_name": "John",
        "last_name": "Smith",
        "email": "john.smith@example.com",
        "phone": "555-6789",
        "birth_date": "1985-05-05",
        "address": "456 Elm St",
        "demographic_segment": "consumer",
        "preferred_language": "en",
    }

    create_response = client.post("/profiles/", json=payload)
    assert create_response.status_code == status.HTTP_201_CREATED
    created = create_response.json()
    assert created["email"] == payload["email"]

    get_response = client.get(f"/profiles/{created['id']}")
    assert get_response.status_code == status.HTTP_200_OK
    assert get_response.json()["id"] == created["id"]


def test_update_profile_via_api():
    payload = {
        "first_name": "John",
        "last_name": "Smith",
        "email": "john.smith2@example.com",
    }

    create_response = client.post("/profiles/", json=payload)
    created = create_response.json()

    update_response = client.put(
        f"/profiles/{created['id']}", json={"phone": "555-0000"}
    )
    assert update_response.status_code == status.HTTP_200_OK
    assert update_response.json()["phone"] == "555-0000"


def test_list_profiles_filtering():
    payload = {
        "first_name": "Alice",
        "last_name": "Johnson",
        "email": "alice.johnson@example.com",
        "demographic_segment": "consumer",
    }
    create_response = client.post("/profiles/", json=payload)
    assert create_response.status_code == status.HTTP_201_CREATED
    created = create_response.json()

    response = client.get("/profiles/?status=active&demographic_segment=consumer")
    assert response.status_code == status.HTTP_200_OK
    profiles = response.json()
    assert any(profile["id"] == created["id"] for profile in profiles)


def test_archive_profile_api_and_events():
    payload = {
        "first_name": "Bob",
        "last_name": "Marley",
        "email": "bob.marley@example.com",
    }
    create_response = client.post("/profiles/", json=payload)
    assert create_response.status_code == status.HTTP_201_CREATED
    created = create_response.json()

    delete_response = client.delete(f"/profiles/{created['id']}")
    assert delete_response.status_code == status.HTTP_204_NO_CONTENT

    get_response = client.get(f"/profiles/{created['id']}")
    assert get_response.status_code == status.HTTP_200_OK
    assert get_response.json()["status"] == "archived"

    events_response = client.get(f"/profiles/{created['id']}/events")
    assert events_response.status_code == status.HTTP_200_OK
    events = events_response.json()
    assert any(e["event_type"] == "archived" for e in events)


def test_audit_review_endpoint():
    payload = {
        "first_name": "Audit",
        "last_name": "User",
        "email": "audit.user@example.com",
        "demographic_segment": "adult",
        "status": "active",
    }
    r = client.post("/profiles/", json=payload)
    assert r.status_code == status.HTTP_201_CREATED
    profile = r.json()
    profile_id = profile["id"]

    # archive the profile
    r = client.delete(f"/profiles/{profile_id}")
    assert r.status_code == status.HTTP_204_NO_CONTENT

    # fetch audit
    r = client.get(f"/profiles/{profile_id}/audit")
    assert r.status_code == status.HTTP_200_OK
    audit = r.json()
    assert isinstance(audit, list)
    assert any(a["event_type"] == "archived" for a in audit)
