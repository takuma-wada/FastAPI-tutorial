FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=true

WORKDIR /src

# Poetry自体のインストール
RUN pip install poetry

# 依存関係ファイルのコピー
COPY pyproject.toml poetry.lock* ./

# ライブラリのインストール（ソースコードをコピーする前に行う！）
RUN poetry install --no-root

# アプリコードのコピー
COPY ./app /src/app

# 実行（compose側で上書きも可能）
CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
