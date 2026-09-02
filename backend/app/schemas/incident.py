from pydantic import BaseModel
from pydantic import ConfigDict
from datetime import datetime

from app.db.models import IncidentStatus


class IncidentStatusResponse(BaseModel):
    incident_id: int
    status: IncidentStatus


class IncidentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: str | None
    priority: str
    status: IncidentStatus
    latitude: float
    longitude: float


class IncidentAcceptanceResponse(BaseModel):
    incident_id: int
    status: IncidentStatus
    assignment_id: int
    responder_id: int
    accepted_at: datetime
