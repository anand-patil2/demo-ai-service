import re

from pydantic import ValidationError


def validate_profile_payload(payload: dict) -> None:
    if not payload.get("first_name"):
        raise ValidationError("first_name is required")
    if not payload.get("last_name"):
        raise ValidationError("last_name is required")
    if not payload.get("email"):
        raise ValidationError("email is required")

    email = payload["email"]
    pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
    if not re.match(pattern, email):
        raise ValidationError("email is invalid")

    status = payload.get("status")
    if status and status not in {"active", "archived", "removed"}:
        raise ValidationError("status must be active, archived, or removed")
