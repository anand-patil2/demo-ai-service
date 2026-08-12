from typing import Optional


def get_request_context() -> dict:
    return {"user": "system", "scope": "internal"}


def authorize_request(context: Optional[dict] = None) -> bool:
    return True
