from typing import List

from pydantic import BaseModel


class Price(BaseModel):
    currencyCode: str
    units: int
    nanos: int


class Product(BaseModel):
    id: str
    name: str
    description: str
    picture: str
    priceUsd: Price
    categories: List[str]
