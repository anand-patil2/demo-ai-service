import pytest

from src.services.customer_profile_service import CustomerProfileService


def test_create_and_retrieve_profile():
    service = CustomerProfileService()
    payload = {
        "first_name": "Jane",
        "last_name": "Doe",
        "email": "jane.doe@example.com",
        "phone": "555-1234",
        "birth_date": "1990-01-01",
        "address": "123 Main St",
        "demographic_segment": "enterprise",
        "preferred_language": "en",
    }

    created = service.create_profile(payload)

    assert created.id
    assert created.first_name == "Jane"
    assert created.email == "jane.doe@example.com"

    retrieved = service.get_profile(created.id)
    assert retrieved is not None
    assert retrieved.email == "jane.doe@example.com"


def test_update_profile():
    service = CustomerProfileService()
    payload = {
        "first_name": "Jane",
        "last_name": "Doe",
        "email": "jane.doe@example.com",
    }
    created = service.create_profile(payload)

    updated = service.update_profile(created.id, {"phone": "555-9876"})
    assert updated is not None
    assert updated.phone == "555-9876"


def test_update_demographic_fields():
    service = CustomerProfileService()
    payload = {
        "first_name": "Jane",
        "last_name": "Doe",
        "email": "jane.doe@example.com",
    }
    created = service.create_profile(payload)

    updated = service.update_profile(
        created.id, {"demographic_segment": "enterprise", "preferred_language": "fr"}
    )
    assert updated is not None
    assert updated.demographic_segment == "enterprise"
    assert updated.preferred_language == "fr"


def test_duplicate_profile_prevention():
    service = CustomerProfileService()
    payload = {
        "first_name": "Jane",
        "last_name": "Doe",
        "email": "jane.doe@example.com",
    }
    service.create_profile(payload)

    with pytest.raises(ValueError):
        service.create_profile(payload)


def test_archive_creates_event():
    service = CustomerProfileService()
    payload = {
        "first_name": "Karl",
        "last_name": "Marx",
        "email": "k.marx@example.com",
    }
    created = service.create_profile(payload)

    archived = service.archive_profile(created.id)
    assert archived is not None
    assert archived.status == "archived"

    events = service.get_profile_events(created.id)
    assert any(e.event_type == "archived" for e in events)
