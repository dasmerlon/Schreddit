from datetime import datetime
from typing import Optional

from pydantic import UUID4, BaseModel

from app.schemas.base import ThingGetterDict


class ThingMetaBase(BaseModel):
    pass


class ThingMetaCreate(BaseModel):
    pass


class ThingMetaUpdate(BaseModel):
    pass


class ThingMeta(BaseModel):
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    uid: UUID4
    author: Optional[str] = None
    count: int
    state: Optional[int]

    class Config:
        getter_dict = ThingGetterDict
        orm_mode = True
