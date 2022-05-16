from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from src.models.complex_test import ComplexTest, OtherObject
from src.helpers.dates import convert_datetime_to_iso_8601


class InComplexTest(BaseModel):
    name: Optional[str]
    other_object: Optional[OtherObject]

    class Config:
        schema_extra = {
            'example': {
                'name': "John Doe",
                'other_object': {
                    'something': "another something"
                }
            }
        }


class UpdateComplexTest(BaseModel):
    name: Optional[str]
    other_object: Optional[OtherObject]

    class Config:
        schema_extra = {
            'example': {
                'name': "Other Doe",
                'other_object': {
                    'something': "another something"
                }
            }
        }


class OutComplexTest(ComplexTest):
    class Config:
        schema_extra = {
            'example': {
                'id': "9276d567-758e-4677-beb3-4992e9b5c5ab",
                'created_at': "2021-12-23T20:41:14Z",
                'updated_at': "2021-12-23T20:41:14Z",
                'name': "John Doe",
                'other_object': {
                    'something': "something"
                }
            },
        }
        json_encoders = {
            datetime: convert_datetime_to_iso_8601,
        }
