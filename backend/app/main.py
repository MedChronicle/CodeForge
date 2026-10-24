from contextlib import asynccontextmanager
from collections.abc import AsyncIterator

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from backend.app.api.router import api_router
from backend.app.core.config import get_settings
from backend.app.core.database import init_db
from backend.app.core.exceptions import DomainError
from backend.app.core.logging import configure_logging
from backend.app.core.rate_limit import enforce_rate_limit


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    configure_logging()
    init_db()
    yield


settings = get_settings()
app = FastAPI(title=settings.app_name, version="0.1.0", lifespan=lifespan)
development_origin_regex = r"https?://(localhost|127\.0\.0\.1)(:\d+)?$" if settings.environment == "development" else None
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_origin, "http://localhost:5173"],
    allow_origin_regex=development_origin_regex,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def rate_limit_middleware(request: Request, call_next):
    if request.url.path not in {"/api/health", "/docs", "/openapi.json", "/redoc"}:
        enforce_rate_limit(request)
    return await call_next(request)


@app.exception_handler(DomainError)
async def domain_error_handler(_: Request, exc: DomainError) -> JSONResponse:
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.message})


@app.get("/")
def root() -> dict[str, str]:
    return {"name": "AlgoForge API", "docs": "/docs", "health": "/api/health"}


app.include_router(api_router)
