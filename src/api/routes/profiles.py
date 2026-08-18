from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel

from src.services.customer_profile_service import CustomerProfileService

router = APIRouter()
service = CustomerProfileService()
service.seed_demo_data()


class ProfileCreateRequest(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone: str | None = None
    birth_date: str | None = None
    address: str | None = None
    demographic_segment: str | None = None
    preferred_language: str | None = None


class ProfileUpdateRequest(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    email: str | None = None
    phone: str | None = None
    birth_date: str | None = None
    address: str | None = None
    demographic_segment: str | None = None
    preferred_language: str | None = None


@router.post("/", status_code=201)
def create_profile(payload: ProfileCreateRequest):
    profile = service.create_profile(payload.model_dump())
    return profile


@router.get("/")
def list_profiles(
    status: str | None = Query(default=None),
    demographic_segment: str | None = Query(default=None),
):
    return service.list_profiles(status=status, demographic_segment=demographic_segment)


@router.get("/{profile_id}")
def get_profile(profile_id: str):
    profile = service.get_profile(profile_id)
    if profile is None:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile


@router.put("/{profile_id}")
def update_profile(profile_id: str, payload: ProfileUpdateRequest):
    profile = service.update_profile(profile_id, payload.model_dump(exclude_none=True))
    if profile is None:
        raise HTTPException(
            status_code=404, detail="Profile not found or cannot be updated"
        )
    return profile


@router.delete("/{profile_id}", status_code=204)
def archive_profile(profile_id: str):
    archived = service.archive_profile(profile_id)
    if archived is None:
        raise HTTPException(status_code=404, detail="Profile not found")
    return {}


@router.get("/{profile_id}/events")
def list_profile_events(profile_id: str):
    events = service.get_profile_events(profile_id)
    return [e.model_dump() for e in events]


@router.get("/{profile_id}/audit")
def profile_audit_review(profile_id: str):
    audit = service.get_profile_audit(profile_id)
    if audit is None:
        raise HTTPException(
            status_code=404, detail="Profile not found or no audit available"
        )
    return audit


@router.post("/seed")
def reset_demo_seed_data():
    seeded = service.reset_demo_data()
    return {
        "status": "seeded",
        "profiles": [profile.model_dump() for profile in seeded],
    }
