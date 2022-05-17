from fastapi import APIRouter
from .complex_test_route import complex_test_router


router = APIRouter()


@router.get("", tags=["API"])
async def index():
    return {'key': "Hello world from API"}


router.include_router(complex_test_router)
