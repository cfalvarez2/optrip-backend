from uuid import uuid4
from pydantic import Field
from pydantic.utils import deep_update
from datetime import datetime
from beanie import Document, Insert, Replace, before_event
from src.helpers.dates import datetime_current, convert_datetime_to_iso_8601


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
        }

    class Settings:
        use_revision = False
