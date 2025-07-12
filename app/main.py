from fastapi import Cookie, Body, FastAPI, Query, Path, Header, Form, File, UploadFile
from typing import Dict, Any, Annotated, Literal
from enum import Enum
from pydantic import BaseModel, Field
from fastapi.responses import HTMLResponse


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
        default=None,
        title="The description of the item",
        max_length=300,
    )
    price: float
    tax: float | None = None


class FilterParams(BaseModel):
    model_config = {"extra": "forbid"}  # 余分なパラメータを制限する

    limit: int = Field(100, gt=0, le=100)
    offset: int = Field(0, ge=0)
    order_by: Literal["created_at", "updated_at"] = "created_at"
    tags: list[str] = []


# クッキーパラメータモデル
class Cookies(BaseModel):
    session_id: str
    fatebook_tracker: str | None = None
    googall_tracker: str | None = None


# ヘッダーパラメータ
class CommonHeaders(BaseModel):
    host: str
    save_data: bool
    if_modified_since: str | None = None
    traceparent: str | None = None
    x_tag: list[str] = []


# フォームデータモデル
class FormData(BaseModel):
    username: str
    password: str
    model_config = {"extra": "forbid"}  # その他の項目を禁止する


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
    q: Annotated[
        str | None, Query(min_length=3, max_length=50, pattern="^fixedquery$")
    ] = None,
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
    user_id: Annotated[int, Path(title="The ID of the item to get", ge=0, le=1000)],
    q: str | None = None,
    item: Annotated[Item | None, Body(embed=True)] = None,
):
    results = {"user_id": user_id}
    if q:
        results.update({"q": q})
    if item:
        results.update({"item": item})
    return results


# クッキーパラメータ
@app.get("/cookie-items/")
async def read_cookie_items(cookies: Annotated[Cookies, Cookie()] = None) -> Cookies:
    return cookies


# ヘッダーパラメータ
@app.get("/header-items/")
async def read_header_items(user_agent: Annotated[CommonHeaders, Header()] = None):
    return {"User-Agent": user_agent}


# ステータスコード
@app.post("/status-code/", status_code=201)
async def statusCode(name: str) -> Dict[str, str]:
    return {"name": name}


# フォームデータ
@app.post("/login/")
async def login(data: Annotated[FormData, Form()]):
    return data


# ファイル取得 小さなファイルの読み取りに適している。コンテンツ全体がメモリに保存される
@app.post("/files/")
async def create_file(file: Annotated[bytes, File()]):
    return {"file_size": len(file)}


# ファイル取得 最大サイズ制限まではメモリに保存され、この制限を超えるとディスクに保存される
@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    return {"filename": file.filename}


# 上二つのテスト用
@app.get("/form")
async def main():
    content = """
<body>
<form action="/files/" enctype="multipart/form-data" method="post">
<input name="files" type="file" multiple>
<input type="submit">
</form>
<form action="/uploadfiles/" enctype="multipart/form-data" method="post">
<input name="files" type="file" multiple>
<input type="submit">
</form>
</body>
    """
    return HTMLResponse(content=content)
