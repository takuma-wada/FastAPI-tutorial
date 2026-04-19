# 変数定義
COMPOSE=docker compose
EXEC_API=$(COMPOSE) exec api

.PHONY: up down build restart ps logs prisma-gen prisma-push prisma-studio setup

# --- Docker操作 ---
up:
	$(COMPOSE) up -d

down:
	$(COMPOSE) down

build:
	$(COMPOSE) build

restart:
	$(MAKE) down
	$(MAKE) up

ps:
	$(COMPOSE) ps

logs:
	$(COMPOSE) logs -f

# --- Prisma操作 ---
prisma-gen:
	$(EXEC_API) prisma generate

prisma-push:
	$(EXEC_API) prisma db push

prisma-studio:
	$(COMPOSE) up -d studio

# --- 初期セットアップ用 ---
setup:
	$(MAKE) build
	$(MAKE) up
	@sleep 5 # DBの起動を待つ
	$(MAKE) prisma-gen
	$(MAKE) prisma-push
	@echo "Setup completed! Visit http://localhost:8000/docs"
