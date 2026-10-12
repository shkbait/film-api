from fastapi import APIRouter
from src.api.films import router as films_router

main_router=APIRouter(
)

main_router.include_router(films_router)