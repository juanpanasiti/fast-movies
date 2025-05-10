from fastapi import APIRouter

from .movie_routes import router as movies_router


router_v1 = APIRouter(prefix='/v1')

router_v1.include_router(movies_router)