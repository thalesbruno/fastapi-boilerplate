from fastapi import FastAPI, Query, status
from typing import Optional
from schemas import Item


app = FastAPI()


@app.get("/items/")
async def read_items(q: Optional[str] = Query(None, max_length=50)):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


@app.post("/items", status_code=status.HTTP_201_CREATED)
async def create_item(item: Item):
    return item


@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    return {'item_id': item_id, **item.dict()}
