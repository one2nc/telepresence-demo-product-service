import json
from difflib import SequenceMatcher
from typing import List

from fastapi import FastAPI, HTTPException

from models import Product

app = FastAPI()

products = {}


@app.on_event("startup")
def load_datastore():
    global products
    with open("./mockdatastore.json", "rb") as f:
        products = json.loads(f.read())


@app.get("/healthz", status_code=201)
async def health():
    return {"message": "Hello from Products Service for a PR-review!"}


@app.get("/products", response_model=List[Product])
async def get_all_products():
    return products["products"]


@app.get("/products/{id}", response_model=Product)
async def get_product_by_id(id: str):
    product = list(filter(lambda x: x["id"] == id, products["products"]))
    try:
        assert product not in [None, []]
        product = product[0]
        return product
    except AssertionError:
        raise HTTPException(status_code=404, detail="Product not found")


@app.get("/products/category/{category}", response_model=List[Product])
async def get_product_by_category(category: str):
    category = category.lower()
    products_ = list(
        filter(lambda x: category in x["categories"], products["products"])
    )
    try:
        assert products_ not in [None, []]
        return products_
    except AssertionError:
        raise HTTPException(
            status_code=404, detail="Products not found for specified category"
        )


@app.get("/products/search/{string}", response_model=List[Product])
async def search_product(string: str):
    def similarity(x):
        return (
            SequenceMatcher(None, x["name"].lower(), string.lower()).ratio()
            > 0.75
        ) or (string.lower() in x["name"].lower())

    products_ = list(filter(similarity, products["products"]))
    try:
        assert products_ not in [None, []]
        return products_
    except AssertionError:
        raise HTTPException(
            status_code=404, detail="Products not found for specified query"
        )
