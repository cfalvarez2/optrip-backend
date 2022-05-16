from fastapi import APIRouter
from src.controllers.complex_tests import test_controller


complex_test_router = APIRouter()
complex_test_router.include_router(
    test_controller, prefix="/complex-tests", tags=["Complex Tests"]
)
