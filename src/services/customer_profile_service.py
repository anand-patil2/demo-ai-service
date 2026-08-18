from __future__ import annotations
from datetime import datetime
import uuid
from typing import Optional

from src.models.customer_profile import CustomerProfile
from src.repositories.customer_profile_repository import CustomerProfileRepository
from src.services.validation import validate_profile_payload
from src.models.profile_event import ProfileEvent


class CustomerProfileService:
    def __init__(self) -> None:
        self.repository = CustomerProfileRepository()

    def seed_demo_data(self) -> list[CustomerProfile]:
        if self.repository.list_profiles():
            return self.repository.list_profiles()

        active_profile = CustomerProfile(
            id=str(uuid.uuid4()),
            first_name="Demo",
            last_name="User",
            email="demo.user@example.com",
            phone="555-0101",
            birth_date="1990-01-01",
            address="123 Demo St",
            demographic_segment="consumer",
            preferred_language="en",
            status="active",
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
        self.repository.save(active_profile)

        archived_profile = CustomerProfile(
            id=str(uuid.uuid4()),
            first_name="Archived",
            last_name="Profile",
            email="archived.user@example.com",
            demographic_segment="enterprise",
            preferred_language="en",
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
        archived_profile.mark_archived()
        self.repository.save(archived_profile)
        self.repository.save_event(
            ProfileEvent(
                id=str(uuid.uuid4()),
                profile_id=archived_profile.id,
                event_type="archived",
                changed_by="system",
                notes="Seeded archived profile",
            )
        )

        return self.repository.list_profiles()

    def reset_demo_data(self) -> list[CustomerProfile]:
        self.repository = CustomerProfileRepository()
        return self.seed_demo_data()

    def create_profile(self, payload: dict) -> CustomerProfile:
        validate_profile_payload(payload)
        existing = self.repository.find_active_by_email(payload["email"])
        if existing:
            raise ValueError("Active profile already exists for this email")

        profile_id = str(uuid.uuid4())
        payload["id"] = profile_id
        payload["created_at"] = datetime.utcnow()
        payload["updated_at"] = datetime.utcnow()
        profile = CustomerProfile(**payload)
        return self.repository.save(profile)

    def get_profile(self, profile_id: str) -> Optional[CustomerProfile]:
        return self.repository.get(profile_id)

    def update_profile(
        self, profile_id: str, changes: dict
    ) -> Optional[CustomerProfile]:
        profile = self.repository.get(profile_id)
        if not profile:
            return None

        if profile.status != "active":
            return None

        payload = profile.model_dump()
        payload.update(changes)
        validate_profile_payload(payload)

        for field, value in changes.items():
            setattr(profile, field, value)
        profile.updated_at = datetime.utcnow()
        return self.repository.save(profile)

    def list_profiles(
        self, status: str | None = None, demographic_segment: str | None = None
    ) -> list[CustomerProfile]:
        return self.repository.list_profiles(
            status=status, demographic_segment=demographic_segment
        )

    def archive_profile(self, profile_id: str) -> Optional[CustomerProfile]:
        profile = self.repository.get(profile_id)
        if not profile:
            return None
        profile.mark_archived()
        saved = self.repository.save(profile)
        # create lifecycle event
        event = ProfileEvent(
            id=str(uuid.uuid4()),
            profile_id=profile_id,
            event_type="archived",
            changed_by="system",
        )
        self.repository.save_event(event)
        return saved

    def delete_profile(self, profile_id: str) -> bool:
        deleted = self.repository.delete(profile_id)
        if deleted:
            event = ProfileEvent(
                id=str(uuid.uuid4()),
                profile_id=profile_id,
                event_type="removed",
                changed_by="system",
            )
            self.repository.save_event(event)
        return deleted

    def get_profile_events(self, profile_id: str) -> list[ProfileEvent]:
        return self.repository.list_events(profile_id)

    def get_profile_audit(self, profile_id: str) -> list[dict]:
        events = self.get_profile_events(profile_id)
        # Return a reviewable representation
        audit = []
        for e in events:
            audit.append(
                {
                    "id": e.id,
                    "event_type": e.event_type,
                    "timestamp": e.timestamp.isoformat(),
                    "changed_by": e.changed_by,
                    "notes": e.notes,
                }
            )
        return audit
