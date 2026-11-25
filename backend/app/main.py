from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.api.v1 import health, instances, mod_profiles
from app.auth.router import router as auth_router

app = FastAPI(
    title="Prism Hub API",
    description="Minecraft launcher backend API",
    version="1.0.0",
    docs_url="/docs" if settings.DEMO_MODE else None,
    redoc_url="/redoc" if settings.DEMO_MODE else None,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router, prefix="/api/v1", tags=["health"])
app.include_router(instances.router, prefix="/api/v1", tags=["instances"])
app.include_router(auth_router, prefix="/api/v1", tags=["auth"])
app.include_router(mod_profiles.router, prefix="/api/v1", tags=["mod-profiles"])


@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "prism-hub-api"}
