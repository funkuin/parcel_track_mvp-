from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import health, parcels
from app.core.config import settings
from app.db.base import Base
from app.db.database import engine
import app.models  # Ensures all models are registered with Base.metadata before create_all


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: create SQLite database tables automatically if they do not exist
    Base.metadata.create_all(bind=engine)
    yield
    # Shutdown logic (none required for SQLite)


# Initialize FastAPI application with lifespan event handler
app = FastAPI(
    title=settings.PROJECT_NAME,
    description=(
        "ParcelTrack Backend API — Parcel registration and tracking system "
        "for transport agencies in Cameroon."
    ),
    version="0.1.0",
    lifespan=lifespan,
)

# Configure CORS for local Vite development frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register route controllers
app.include_router(health.router)
app.include_router(parcels.router, prefix=settings.API_PREFIX)
