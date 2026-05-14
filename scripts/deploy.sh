#!/bin/bash
# ── Скрипт деплоя — выполняется НА СЕРВЕРЕ ──
# Вызывается через: ssh user@host 'bash -s' < scripts/deploy.sh

set -e

DEPLOY_DIR="/opt/school-site"
REPO_URL="http://a5e802c07dcd.vps.myjino.ru:49179/dchmilenko/school-porject.git"
BRANCH="develop"

echo "══════════════════════════════════════"
echo "  Деплой школьного сайта"
echo "  $(date '+%Y-%m-%d %H:%M:%S')"
echo "══════════════════════════════════════"

# 1. Клонировать или обновить репозиторий
if [ ! -d "$DEPLOY_DIR" ]; then
    echo "→ Клонирование репозитория..."
    git clone -b "$BRANCH" "$REPO_URL" "$DEPLOY_DIR"
else
    echo "→ Обновление репозитория..."
    cd "$DEPLOY_DIR"
    git fetch origin
    git reset --hard "origin/$BRANCH"
fi

cd "$DEPLOY_DIR"

# 2. Собрать и запустить контейнеры
echo "→ Сборка Docker-контейнеров..."
docker compose -f docker-compose.prod.yml build

echo "→ Запуск контейнеров..."
docker compose -f docker-compose.prod.yml up -d

# 3. Ждём готовности БД
echo "→ Ждём готовности базы данных..."
sleep 10

# 4. Миграции и статика (выполняются внутри контейнера через command)
echo "→ Проверяем статус контейнеров..."
docker compose -f docker-compose.prod.yml ps

# 5. Загрузка seed data (раскомментировать при первом деплое)
# docker compose -f docker-compose.prod.yml exec -T backend python manage.py seed_data

echo ""
echo "✅ Деплой завершён успешно!"
echo "Сайт: http://test-project.space"
echo "══════════════════════════════════════"
