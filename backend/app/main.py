from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from app.api.dispatch import router as dispatch_router
from app.api.incidents import router as incidents_router
from app.api.responders import router as responders_router
from app.core.config import settings
from app.db.database import AsyncSessionLocal, init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(
    title=settings.app_name,
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(dispatch_router)
app.include_router(incidents_router)
app.include_router(responders_router)


@app.get("/health")
async def health_check():
    return {
        "status": "ok",
        "database": "configured",
    }


@app.get("/health/db")
async def database_health_check():
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            text("SELECT PostGIS_Version();")
        )

        postgis_version = result.scalar()

    return {
        "status": "ok",
        "database": "connected",
        "postgis_version": postgis_version,
    }