# FastAPI Todo App

FastAPI と Prisma (Python)、PostgreSQL を使用した Todo アプリケーションのバックエンド API デモプロジェクトです。

## 使用技術 (Tech Stack)

* **フレームワーク**: [FastAPI](https://fastapi.tiangolo.com/)
* **データベース**: [PostgreSQL](https://www.postgresql.org/)
* **ORM**: [Prisma Client Python](https://prisma-client-py.readthedocs.io/en/stable/)
* **パッケージマネージャ**: [Poetry](https://python-poetry.org/)
* **コンテナ**: [Docker](https://www.docker.com/) & Docker Compose

## 環境構築と実行方法

Docker がインストールされていることを確認し、プロジェクトのルートディレクトリで以下のコマンドを実行します。

```bash
# .envファイルを作成（必要に応じて中身を書き換えてください）
cp .env.example .env

# Dockerコンテナのビルドと起動（バックグラウンド）
docker-compose up -d --build
```

### データベースのスキーマ同期
コンテナが起動したら、初回はデータベースにスキーマを反映させる必要があります。`api` コンテナ内で Prisma のマイグレーションコマンド（もしくは `db push`）を実行します。

```bash
# コンテナ内で db push を実行
docker-compose exec api prisma db push
```

## エンドポイントのアクセス先

Docker コマンド起動後、以下の URL にアクセスできます。

* **API 自動生成ドキュメント (Swagger UI)**:
  [http://localhost:8000/docs](http://localhost:8000/docs)
  ブラウザからこのURLにアクセスすると、APIの仕様確認やテスト実行が直感的に行なえます。

* **Prisma Studio (DB GUI 管理ツール)**:
  [http://localhost:5555](http://localhost:5555)
  データベースの中身をブラウザ上で直接確認・編集・削除できます。

* **APIのベースURL**:
  [http://localhost:8000](http://localhost:8000)
    * (例) `http://localhost:8000/hello`

## その他コマンド

コンテナ終了・削除:
```bash
docker-compose down
```

コンテナ内でPoetryを使って追加パッケージをインストールした場合などは、イメージの再ビルドを行ってください。
```bash
docker-compose build
```
