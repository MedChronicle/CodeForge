# AlgoForge database migrations

The development path uses `Base.metadata.create_all()` from
`backend.app.core.database.init_db()` so a fresh checkout can run without an
external migration binary. The SQLAlchemy models are kept migration-ready:
production deployments should add Alembic revisions under `versions/`, run them
before the API starts, and disable automatic table creation in the lifespan.
