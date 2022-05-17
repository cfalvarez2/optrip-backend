from fastapi import APIRouter, Body, HTTPException
from fastapi.encoders import jsonable_encoder
from typing import List
from src.models.complex_test import ComplexTest
from .schema import InComplexTest, UpdateComplexTest, OutComplexTest


test_controller = APIRouter()


@test_controller.get(
    "", response_model=List[OutComplexTest], response_model_by_alias=False
)
async def get_complex_tests():
    tests: List[ComplexTest] = await ComplexTest.find_all().to_list()
    return jsonable_encoder(tests, by_alias=False)


@test_controller.post(
    "", response_model=OutComplexTest, status_code=201,
    response_model_by_alias=False
)
async def create_task(test: InComplexTest = Body(...)):
    new_test_model: ComplexTest = ComplexTest(**test.dict())
    await new_test_model.insert()
    return new_test_model.dict()


@test_controller.get(
    "/{test_id}", response_model=OutComplexTest, response_model_by_alias=False
)
async def get_task(test_id: str):
    test_model: ComplexTest = await ComplexTest.get(test_id)
    if not test_model:
        raise HTTPException(status_code=404, detail="Test not found")
    return test_model.dict()


@test_controller.patch(
    "/{test_id}", response_model=OutComplexTest, response_model_by_alias=False
)
async def update_task(test_id: str, test: UpdateComplexTest = Body(...)):
    test_model: ComplexTest = await ComplexTest.get(test_id)
    if not test_model:
        raise HTTPException(status_code=404, detail="Test not found")
    test_model = await test_model.update(test.dict(exclude_unset=True))
    return test_model.dict()
