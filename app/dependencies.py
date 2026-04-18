from typing import Annotated


async def common_parameters(
    q: str | None = None,
    skip: int = 0,
    limit: int = 100
):
    return {"q": q, "skip": skip, "limit": limit}

# 型エイリアスを使って、Annotatedを短縮することも可能です
CommonDep = Annotated[dict, "This is a dependency"]
