from fastapi import FastAPI

from app.api import router

app = FastAPI(title="VPN Panel HostAgent", version="0.1.0")
app.include_router(router, prefix="/internal/v1")


@app.get("/health", tags=["system"])
async def health() -> dict[str, str]:
    return {"status": "ok"}
