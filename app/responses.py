from typing import Mapping, Iterable
from pydantic import BaseModel

"""
Considerations:
Which JSON response standard to use?
- JSON API http://jsonapi.org/
- JSend https://github.com/omniti-labs/jsend
- Custom JSON response
"""


class BaseResponse(BaseModel):
    status_code: int
    body: Mapping

    class Config:
        orm_mode = False


class PaginatedResponse(BaseResponse):
    page: int
    limit: int
    skip: int

    class Config:
        orm_mode = False
