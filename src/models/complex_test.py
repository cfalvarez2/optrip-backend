from pydantic import BaseModel, Field
from typing import Optional
from . import Main


class OtherObject(BaseModel):
    something: Optional[str] = "something"


class ComplexTest(Main):
    name: str
    other_object: OtherObject = Field(..., alias='otherObject')

    class Collection:
        name = "complexTests"
