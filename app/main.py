from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from app.api.routes import router
from app.core.config import settings

app = FastAPI(
    title=settings.app_name,
    description="Multi-agent orchestration platform with Safe AI validation and audit governance",
    version=settings.app_version,
)

app.include_router(router, prefix="/api/v1")

@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse(url="/docs")


@app.get("/health")
async def health_check():
    return {"status": "ok", "version": settings.app_version}