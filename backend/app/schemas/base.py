from datetime import datetime

from pydantic import BaseModel


class Pagination(BaseModel):
    after: datetime
    before: datetime
    limit: int
