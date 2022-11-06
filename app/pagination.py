from typing import TypeVar, Generic
from fastapi_pagination import Page as BasePage
from fastapi_pagination import Params as BaseParams


# Building fast api pagination with custom params (size=100)

T = TypeVar("T")


class Params(BaseParams):
    size: int = 100


class Page(BasePage[T], Generic[T]):
    __params_type__ = Params
