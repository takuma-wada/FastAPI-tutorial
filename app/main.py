from fastapi import Body, FastAPI, Query, Path
from typing import Dict, Any, Annotated, Literal
from enum import Enum
from pydantic import BaseModel, Field


# Enum class
class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"


# リクエストbody sample パラメーターと考え方は同じ version 3.10
class Item(BaseModel):
    name: str
    description: str | None = Field(
        # open apiに説明を記載できる
        default=None, title="The description of the item", max_length=300
    )
    price: float
    tax: float | None = None


class FilterParams(BaseModel):
    model_config = {"extra": "forbid"}  # 余分なパラメータを制限する

    limit: int = Field(100, gt=0, le=100)
    offset: int = Field(0, ge=0)
    order_by: Literal["created_at", "updated_at"] = "created_at"
    tags: list[str] = []


# FastAPIアプリケーションのインスタンスを作成
app = FastAPI()

# APIドキュメント(openapi) エンドポイント
# /redoc or /docs


# ルートエンドポイント
@app.get("/")
async def read_root() -> Dict[str, str]:
    return {"message": "こんにちは, FastAPI!"}


# パスパラメータを持つエンドポイント
@app.get("/items/{item_id}")
async def read_item(item_id: int, q: str | None = None) -> Dict[str, Any]:
    return {"item_id": item_id, "q": q}


# enumで型アノテーションしたエンドポイント
@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name is ModelName.alexnet:  # 比較
        return {"model_name": model_name, "message": "Deep Learning FTW!"}

    if model_name.value == "lenet":  # model_name.valueでも取得可能
        return {"model_name": model_name, "message": "LeCNN all the images"}

    return {"model_name": model_name, "message": "Have some residuals"}


# クエリパラメーター
@app.get("/user/items/{item_id}")
async def read_user_item(
    item_id: str, needy: str, skip: int = 0, limit: int | None = None
):  # Noneでオプショナル、なければ必須。デフォルト値指定も可能
    item = {"item_id": item_id, "needy": needy, "skip": skip, "limit": limit}
    return item


# リクエストbody
@app.post("/items/")
async def create_item(item: Item):
    # item.name.capitalize //pydanticを受け取るとエディターによる型ヒントと補完が関数内で利用可能
    item_dict = item.dict()
    if item.tax is not None:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict


# リクエストbody + パスパラメータ(上と同じ要領でクエリパラメータも指定できる)
@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    return {"item_id": item_id, **item.dict()}


# クエリパラメータと文字列の検証
@app.get("/items/")
async def read_items(q: Annotated[str | None, Query(max_length=50)] = None):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return


# 正規表現の追加
@app.get("/regex-items/")
async def read_regex_items(
    q: Annotated[str | None, Query(
        min_length=3,
        max_length=50,
        pattern="^fixedquery$"
    )] = None
):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return


# クエリパラメータモデル
@app.get("/query-items/")
async def read_query_items(filter_query: Annotated[FilterParams, Query()]):
    return filter_query


# ファストAPIボディ - 複数のパラメータ
@app.put("/request-body/{user_id}")
async def user_data(
    user_id: Annotated[
        int,
        Path(title="The ID of the item to get", ge=0, le=1000)
    ],
    q: str | None = None,
    item: Annotated[Item | None, Body(embed=True)] = None
):
    results = {"user_id": user_id}
    if q:
        results.update({"q": q})
    if item:
        results.update({"item": item})
    return results
