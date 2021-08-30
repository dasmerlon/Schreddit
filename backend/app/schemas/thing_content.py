from typing import Optional

from pydantic import BaseModel, constr


class ThingContentBase(BaseModel):
    text: Optional[constr(min_length=1, strip_whitespace=True)] = None


class ThingContentCreate(ThingContentBase):
    text: constr(min_length=1, strip_whitespace=True)


class ThingContentUpdate(ThingContentBase):
    pass


class ThingContent(ThingContentBase):
    class Config:
        orm_mode = True
