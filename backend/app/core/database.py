from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from backend.app.core.config import get_settings


settings = get_settings()
connect_args = {"check_same_thread": False} if settings.database_url.startswith("sqlite") else {}
engine = create_engine(settings.database_url, connect_args=connect_args, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, expire_on_commit=False)


def get_db() -> Generator[Session, None, None]:
    """Yield a request-scoped SQLAlchemy session and always close it."""
    database = SessionLocal()
    try:
        yield database
    finally:
        database.close()


def init_db() -> None:
    """Create all tables for local development.

    Production deployments can replace this with Alembic migrations without
    changing the model layer.
    """
    from backend.app.models.base import Base
    from backend.app.models import problem, progress, refresh_token, resource, sheet, topic, user, user_profile

    _ = (problem, progress, refresh_token, resource, sheet, topic, user, user_profile)
    Base.metadata.create_all(bind=engine)
