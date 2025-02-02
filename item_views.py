from typing import Annotated

from fastapi import APIRouter, Path


router = APIRouter(prefix="/items", tags=["Items"])


@router.get("")
def list_items():
    return {
        "Item1",
        "item2",
        "item3",
    }
    
    
# Порядок решает!!! Если бы это было после предыдущего роута, то сначала шла бы проверка на тип данных item_id !!!
@router.get("/latest")
def get_latest_item():
    return {"item": {"id": 0, "name": "latest"}}


@router.get("/{item_id}")
def get_item_by_id(item_id: Annotated[int, Path(ge=1, lt=1_000_000)]):
    return {
        "item": {
            "id": item_id
        }
    }