# ベースとなるPythonイメージを指定
FROM python:3.11-slim

# 環境変数を設定
ENV PYTHONUNBUFFERED 1

# コンテナ内での作業ディレクトリを設定
WORKDIR /code

# 必要なライブラリをインストールするために requirements.txt をコピー
COPY requirements.txt .

# pipを使ってrequirements.txtに記載されたライブラリをインストール
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# アプリケーションコードをコンテナにコピー
COPY ./app /code/app
