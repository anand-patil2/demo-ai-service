from __future__ import annotations
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class CustomerProfile(BaseModel):
    id: str
    first_name: str
    last_name: str
    email: str
    phone: Optional[str] = None
    birth_date: Optional[str] = None
    address: Optional[str] = None
    demographic_segment: Optional[str] = None
    preferred_language: Optional[str] = None
    status: str = Field(default="active")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    archived_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None

    def mark_archived(self) -> None:
        self.status = "archived"
        self.archived_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

    def mark_removed(self) -> None:
        self.status = "removed"
        self.deleted_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
