import json

from app.db.redis import redis_client


DISPATCH_QUEUE = "resqgrid:dispatch_queue"


async def enqueue_dispatch(incident_id: int) -> None:
    job = {
        "incident_id": incident_id,
    }

    await redis_client.rpush(
        DISPATCH_QUEUE,
        json.dumps(job),
    )


async def dequeue_dispatch():
    item = await redis_client.lpop(
        DISPATCH_QUEUE,
    )

    if item is None:
        return None

    return json.loads(item)
