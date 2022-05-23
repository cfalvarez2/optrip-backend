from uuid import uuid4
from pydantic import BaseModel, Field, validator
from pydantic.utils import deep_update
from datetime import datetime, timedelta
from typing import List
from bson.objectid import ObjectId
from beanie import Document, Insert, Replace, before_event
from src.helpers.dates import datetime_current, convert_datetime_to_iso_8601
from functools import reduce


class Main(Document):
    id: str = Field(default_factory=uuid4, alias="_id", unique=True, pk=True)
    created_at: datetime = Field(
        default_factory=datetime_current, alias="createdAt"
    )
    updated_at: datetime = Field(
        default_factory=datetime_current, alias="updatedAt"
    )

    def change(self, data: dict) -> Document:
        new_data = deep_update(self.dict(), data)
        self = self.__class__(**new_data)
        return self

    async def update(self, data: dict = {}) -> Document:
        if data:
            self = self.change(data)
        del self.revision_id
        await self.replace()
        return self

    @before_event(Insert)
    def stringify_id(self) -> None:
        self.id = str(self.id)

    @before_event(Replace)
    def change_update_date(self) -> None:
        self.stringify_id()
        self.updated_at = datetime_current()

    class Config:
        json_encoders = {
            datetime: convert_datetime_to_iso_8601,
            ObjectId: str,
        }

    class Settings:
        use_revision = False

class Company(BaseModel):
    id: str = Field(default_factory=uuid4, alias="_id", unique=True, pk=True)
    name: str

class City(BaseModel):
    id: str = Field(default_factory=uuid4, alias="_id", unique=True, pk=True)
    name: str 
    countryCode: str

class RouteLeg(BaseModel):
    origin: City
    destination: City
    departure: datetime
    arrival: datetime
    travel_time: timedelta
    price: int
    type: str
    companyId: Company.id

    @validator('type')
    def type_match(cls, value):
        if not value in ['flight', 'bus']:
            raise ValueError('type must be in [flight, bus]')
        return value


class Route(Main):
    legs: List[RouteLeg]

    def getTotalCost(self):
        return reduce(lambda a, b: a.price + b.price, self.legs)
    
    def getTotalTravelTime(self):
        return reduce(lambda a, b: a.travel_time + b.travel_time, self.legs)