from __future__ import annotations
from typing import Dict, Optional

from src.models.customer_profile import CustomerProfile
from src.models.profile_event import ProfileEvent


class CustomerProfileRepository:
    def __init__(self) -> None:
        self._profiles: Dict[str, CustomerProfile] = {}
        self._events: Dict[str, list[ProfileEvent]] = {}

    def save(self, profile: CustomerProfile) -> CustomerProfile:
        self._profiles[profile.id] = profile
        return profile

    def get(self, profile_id: str) -> Optional[CustomerProfile]:
        profile = self._profiles.get(profile_id)
        if profile and profile.status == "removed":
            return None
        return profile

    def find_active_by_email(self, email: str) -> Optional[CustomerProfile]:
        for profile in self._profiles.values():
            if profile.email == email and profile.status == "active":
                return profile
        return None

    def list_profiles(self, status: str | None = None, demographic_segment: str | None = None) -> list[CustomerProfile]:
        results = []
        for profile in self._profiles.values():
            if status and profile.status != status:
                continue
            if demographic_segment and profile.demographic_segment != demographic_segment:
                continue
            results.append(profile)
        return results

    def delete(self, profile_id: str) -> bool:
        profile = self._profiles.get(profile_id)
        if not profile:
            return False
        profile.mark_removed()
        self._profiles[profile_id] = profile
        return True

    def save_event(self, event: ProfileEvent) -> ProfileEvent:
        events = self._events.setdefault(event.profile_id, [])
        events.append(event)
        return event

    def list_events(self, profile_id: str) -> list[ProfileEvent]:
        return list(self._events.get(profile_id, []))
