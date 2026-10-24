from fastapi import APIRouter

from backend.app.api.routes import admin, auth, health, ml, problems, progress, progress_analytics, resources, revision, sheet, topics, users


api_router = APIRouter(prefix="/api")
api_router.include_router(health.router)
api_router.include_router(auth.router)
api_router.include_router(users.router)
api_router.include_router(topics.router)
api_router.include_router(problems.router)
api_router.include_router(resources.router)
api_router.include_router(sheet.router)
api_router.include_router(progress.router)
api_router.include_router(revision.router)
api_router.include_router(ml.router)
api_router.include_router(progress_analytics.router)
api_router.include_router(admin.router)
