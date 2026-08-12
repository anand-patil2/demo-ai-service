from __future__ import annotations
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class ProfileEvent(BaseModel):
    id: str
    profile_id: str
    event_type: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    changed_by: str
    notes: Optional[str] = None
