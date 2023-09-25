from fastapi import APIRouter

from app.api.api_v1.endpoints import latex

api_router = APIRouter()
api_router.include_router(latex.router, prefix="/latex", tags=["latex"])
