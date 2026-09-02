from fastapi import APIRouter

from app.services.dispatch_queue import enqueue_dispatch

router = APIRouter(
    prefix="/dispatch",
    tags=["Dispatch"],
)


@router.post("/{incident_id}")
async def dispatch_incident(incident_id: int):
    await enqueue_dispatch(incident_id)

    return {
        "status": "queued",
        "incident_id": incident_id,
    }
