from fastapi import APIRouter
from .routes import index, v1


router = APIRouter()

# Import routers
router.include_router(index, include_in_schema=False)
router.include_router(v1.router, prefix="/v1")
