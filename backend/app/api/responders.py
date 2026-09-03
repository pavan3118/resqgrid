from fastapi import APIRouter
from sqlalchemy import text

from app.db.database import AsyncSessionLocal

router = APIRouter(prefix="/responders", tags=["Responders"])


@router.get("")
async def get_responders():
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            text(
                """
                SELECT
                    r.id,
                    r.name,
                    r.phone,
                    r.responder_type,
                    r.status,
                    rl.latitude,
                    rl.longitude,
                    rl.updated_at
                FROM responders r
                LEFT JOIN responder_locations rl
                    ON r.id = rl.responder_id
                ORDER BY r.id
                """
            )
        )

        responders = [
            {
                "id": row.id,
                "name": row.name,
                "phone": row.phone,
                "responder_type": row.responder_type,
                "status": row.status,
                "latitude": row.latitude,
                "longitude": row.longitude,
                "updated_at": row.updated_at,
            }
            for row in result
        ]

    return {"responders": responders}
