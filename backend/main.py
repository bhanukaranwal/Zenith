from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

from backend.core.config import settings
from backend.core.database import engine, Base
from backend.core.telemetry import setup_telemetry
from backend.api import auth, projects, datasets, features, experiments, models, deploy, monitor, agents, prompts


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    if settings.OTEL_ENABLED:
        setup_telemetry()
    
    yield
    
    await engine.dispose()


app = FastAPI(
    title="Zenith ML Platform",
    description="The Zenith of Machine Learning Platforms - AI-first MLOps for 2026",
    version="0.1.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if settings.OTEL_ENABLED:
    FastAPIInstrumentor.instrument_app(app)

app.include_router(auth.router, prefix="/api/v1/auth", tags=["authentication"])
app.include_router(projects.router, prefix="/api/v1/projects", tags=["projects"])
app.include_router(datasets.router, prefix="/api/v1/datasets", tags=["datasets"])
app.include_router(features.router, prefix="/api/v1/features", tags=["features"])
app.include_router(experiments.router, prefix="/api/v1/experiments", tags=["experiments"])
app.include_router(models.router, prefix="/api/v1/models", tags=["models"])
app.include_router(deploy.router, prefix="/api/v1/deployments", tags=["deployments"])
app.include_router(monitor.router, prefix="/api/v1/monitoring", tags=["monitoring"])
app.include_router(agents.router, prefix="/api/v1/agents", tags=["agents"])
app.include_router(prompts.router, prefix="/api/v1/prompts", tags=["prompts"])


@app.get("/health")
async def health_check():
    return JSONResponse(
        content={
            "status": "healthy",
            "version": "0.1.0",
            "service": "zenith-backend"
        }
    )


@app.get("/")
async def root():
    return {
        "message": "Welcome to Zenith ML Platform",
        "docs": "/docs",
        "health": "/health"
    }
