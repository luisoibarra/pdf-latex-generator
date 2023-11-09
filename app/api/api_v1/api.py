from fastapi import APIRouter

from api.api_v1.endpoints import latex
from api.api_v1.endpoints import word

api_router = APIRouter()
api_router.include_router(latex.router, prefix="/latex", tags=["latex", "tex"])
api_router.include_router(word.router, prefix="/word", tags=["word", "docx"])
