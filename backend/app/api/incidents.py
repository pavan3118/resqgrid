from datetime import datetime, timezone

from fastapi import APIRouter, HTTPException
from sqlalchemy import desc, select, update

from app.db.database import AsyncSessionLocal
from app.db.models import (
    Incident,
    IncidentAssignment,
    IncidentStatus,
    Responder,
)
from app.schemas.incident import IncidentAcceptanceResponse, IncidentResponse


router = APIRouter(
    prefix="/incidents",
    tags=["Incidents"],
)


@router.get("/{incident_id}", response_model=IncidentResponse)
async def get_incident(incident_id: int):
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(Incident).where(Incident.id == incident_id)
        )
        incident = result.scalar_one_or_none()

    if incident is None:
        raise HTTPException(status_code=404, detail="Incident not found")

    return incident


@router.post(
    "/{incident_id}/accept",
    response_model=IncidentAcceptanceResponse,
)
async def accept_incident(incident_id: int):
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(Incident).where(Incident.id == incident_id)
        )
        incident = result.scalar_one_or_none()

        if incident is None:
            raise HTTPException(status_code=404, detail="Incident not found")

        if incident.status != IncidentStatus.ASSIGNED:
            raise HTTPException(
                status_code=409,
                detail="Incident must be ASSIGNED before acceptance",
            )

        assignment_result = await session.execute(
            select(IncidentAssignment)
            .where(IncidentAssignment.incident_id == incident_id)
            .order_by(desc(IncidentAssignment.id))
            .limit(1)
        )
        assignment = assignment_result.scalar_one_or_none()

        if assignment is None:
            raise HTTPException(
                status_code=409,
                detail="Incident has no assignment",
            )

        accepted_at = datetime.now(timezone.utc)
        assignment.accepted_at = accepted_at
        incident.status = IncidentStatus.ACCEPTED

        await session.commit()

    return {
        "incident_id": incident.id,
        "status": incident.status,
        "assignment_id": assignment.id,
        "responder_id": assignment.responder_id,
        "accepted_at": accepted_at,
    }


@router.post(
    "/{incident_id}/en-route",
    response_model=IncidentAcceptanceResponse,
)
async def mark_incident_en_route(incident_id: int):
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(Incident).where(Incident.id == incident_id)
        )
        incident = result.scalar_one_or_none()

        if incident is None:
            raise HTTPException(status_code=404, detail="Incident not found")

        if incident.status != IncidentStatus.ACCEPTED:
            raise HTTPException(
                status_code=409,
                detail="Incident must be ACCEPTED before going en-route",
            )

        assignment_result = await session.execute(
            select(IncidentAssignment)
            .where(IncidentAssignment.incident_id == incident_id)
            .order_by(desc(IncidentAssignment.id))
            .limit(1)
        )
        assignment = assignment_result.scalar_one_or_none()

        if assignment is None:
            raise HTTPException(
                status_code=409,
                detail="Incident has no assignment",
            )

        incident.status = IncidentStatus.EN_ROUTE
        await session.commit()

    return {
        "incident_id": incident.id,
        "status": incident.status,
        "assignment_id": assignment.id,
        "responder_id": assignment.responder_id,
        "accepted_at": assignment.accepted_at,
    }


@router.post(
    "/{incident_id}/on-scene",
    response_model=IncidentAcceptanceResponse,
)
async def mark_incident_on_scene(incident_id: int):
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(Incident).where(Incident.id == incident_id)
        )
        incident = result.scalar_one_or_none()

        if incident is None:
            raise HTTPException(status_code=404, detail="Incident not found")

        if incident.status != IncidentStatus.EN_ROUTE:
            raise HTTPException(
                status_code=409,
                detail="Incident must be EN_ROUTE before going on-scene",
            )

        assignment_result = await session.execute(
            select(IncidentAssignment)
            .where(IncidentAssignment.incident_id == incident_id)
            .order_by(desc(IncidentAssignment.id))
            .limit(1)
        )
        assignment = assignment_result.scalar_one_or_none()

        if assignment is None:
            raise HTTPException(
                status_code=409,
                detail="Incident has no assignment",
            )

        incident.status = IncidentStatus.ON_SCENE
        await session.commit()

    return {
        "incident_id": incident.id,
        "status": incident.status,
        "assignment_id": assignment.id,
        "responder_id": assignment.responder_id,
        "accepted_at": assignment.accepted_at,
    }


@router.post(
    "/{incident_id}/resolve",
    response_model=IncidentAcceptanceResponse,
)
async def resolve_incident(incident_id: int):
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(Incident).where(Incident.id == incident_id)
        )
        incident = result.scalar_one_or_none()

        if incident is None:
            raise HTTPException(status_code=404, detail="Incident not found")

        if incident.status != IncidentStatus.ON_SCENE:
            raise HTTPException(
                status_code=409,
                detail="Incident must be ON_SCENE before resolution",
            )

        assignment_result = await session.execute(
            select(IncidentAssignment)
            .where(IncidentAssignment.incident_id == incident_id)
            .order_by(desc(IncidentAssignment.id))
            .limit(1)
        )
        assignment = assignment_result.scalar_one_or_none()

        if assignment is None:
            raise HTTPException(
                status_code=409,
                detail="Incident has no assignment",
            )

        incident.status = IncidentStatus.RESOLVED
        await session.execute(
            update(Responder)
            .where(Responder.id == assignment.responder_id)
            .values(status="AVAILABLE")
        )
        await session.commit()

    return {
        "incident_id": incident.id,
        "status": incident.status,
        "assignment_id": assignment.id,
        "responder_id": assignment.responder_id,
        "accepted_at": assignment.accepted_at,
    }