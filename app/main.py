from fastapi import FastAPI
from typing import Dict, Any, Union
from enum import Enum
from pydantic import BaseModel

# Enum class
class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"

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
    if model_name is ModelName.alexnet: # 比較
        return {"model_name": model_name, "message": "Deep Learning FTW!"}

    if model_name.value == "lenet": # model_name.valueでも取得可能
        return {"model_name": model_name, "message": "LeCNN all the images"}

    return {"model_name": model_name, "message": "Have some residuals"}

# クエリパラメーター
@app.get("/user/items/{item_id}")
async def read_user_item(
    item_id: str, needy: str, skip: int = 0, limit: Union[int, None] = None
): # Noneでオプショナル、なければ必須。デフォルト値指定も可能
    item = {"item_id": item_id, "needy": needy, "skip": skip, "limit": limit}
    return item
