import asyncio

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings
from app.db.redis import redis_client
from app.services.dispatch_queue import dequeue_dispatch
from app.services.dispatch_service import assign_nearest_responder

engine = create_async_engine(
    settings.database_url,
    echo=False,
)

AsyncSessionLocal = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def process_dispatch_job(job: dict):
    incident_id = job["incident_id"]

    async with AsyncSessionLocal() as session:
        result = await assign_nearest_responder(
            session,
            incident_id,
        )

        print(
            f"Processed incident {incident_id}: {result}"
        )


async def worker():
    print("Dispatch worker started")

    while True:
        try:
            job = await dequeue_dispatch()

            if job is None:
                await asyncio.sleep(1)
                continue

            await process_dispatch_job(job)

        except Exception as exc:
            print(
                f"Worker error: {exc}"
            )

            await asyncio.sleep(2)


async def main():
    try:
        await worker()
    finally:
        await redis_client.aclose()
        await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
