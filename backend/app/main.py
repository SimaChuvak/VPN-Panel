from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.router import router
from app.core.config import settings
from app.core.logging import configure_logging
from app.db.session import SessionLocal
from app.services.bootstrap import create_initial_admin

configure_logging()


@asynccontextmanager
async def lifespan(_: FastAPI):
    async with SessionLocal() as session:
        await create_initial_admin(session)
    yield


app = FastAPI(title="VPN Panel API", version="0.1.0", lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(router, prefix="/api/v1")
