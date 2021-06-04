from typing import Optional

from pydantic import UUID4, BaseModel


class Pagination(BaseModel):
    after: Optional[UUID4] = None
    before: Optional[UUID4] = None
    limit: int
