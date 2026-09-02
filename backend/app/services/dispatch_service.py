from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession


async def assign_nearest_responder(
    session: AsyncSession,
    incident_id: int,
):
    query = text(
        """
        WITH nearest_responder AS (
            SELECT
                r.id AS responder_id,
                i.id AS incident_id
            FROM incidents i
            JOIN responder_locations rl
                ON TRUE
            JOIN responders r
                ON r.id = rl.responder_id
            WHERE i.id = :incident_id
              AND r.status = 'AVAILABLE'
              AND i.status = 'SEARCHING'
              AND ST_DWithin(
                  rl.location,
                  i.location,
                  5000
              )
            ORDER BY ST_Distance(
                rl.location,
                i.location
            )
            LIMIT 1
        )
        INSERT INTO incident_assignments (
            incident_id,
            responder_id
        )
        SELECT
            incident_id,
            responder_id
        FROM nearest_responder
        RETURNING id, incident_id, responder_id, assigned_at;
        """
    )

    result = await session.execute(
        query,
        {"incident_id": incident_id},
    )

    assignment = result.fetchone()

    if assignment is None:
        return None

    await session.execute(
        text(
            """
            UPDATE incidents
            SET status = 'ASSIGNED'
            WHERE id = :incident_id
              AND status = 'SEARCHING'
            """
        ),
        {"incident_id": incident_id},
    )

    await session.execute(
        text(
            """
            UPDATE responders
            SET status = 'BUSY'
            WHERE id = :responder_id
              AND status = 'AVAILABLE'
            """
        ),
        {"responder_id": assignment.responder_id},
    )

    await session.commit()

    return {
        "assignment_id": assignment.id,
        "incident_id": assignment.incident_id,
        "responder_id": assignment.responder_id,
        "assigned_at": assignment.assigned_at,
    }
