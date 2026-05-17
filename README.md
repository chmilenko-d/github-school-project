# Универсальный конструктор школьных сайтов

Веб-приложение для школы с управлением контентом через Django Admin. Headless CMS: Django (GraphQL API) + Vue 3 SPA.

- **Сайт:** http://info-project.site
- **Админка:** http://info-project.site/admin/
- **Репозиторий:** http://a5e802c07dcd.vps.myjino.ru:49179/dchmilenko/school-porject

## Стек
- **Backend:** Django 5, Graphene (GraphQL), PostgreSQL 16, Gunicorn
- **Frontend:** Vite 7, Vue 3, Vue Router, Apollo Client
- **Infrastructure:** Docker Compose (3 контейнера: PostgreSQL + Django + Nginx), Jino VPS

## Структура проекта
```
myproject/              Django бэкенд (models, schema GraphQL, admin)
frontend/               Vue 3 SPA (компоненты, роутинг, Apollo Client)
nginx/                  Nginx reverse proxy (конфиг + Dockerfile)
scripts/                Скрипты SSH и деплоя
docker-compose.yml      Dev: PostgreSQL + backend
docker-compose.prod.yml Prod: PostgreSQL + backend + nginx
dev.env / prod.env      Переменные окружения (prod.env в .gitignore)
docs/                   Документация проекта
```

## Репозиторий
```bash
# Клонирование
git clone http://a5e802c07dcd.vps.myjino.ru:49179/dchmilenko/school-porject.git
cd school-porject
git checkout develop
```

Ветки:
- `main` — стабильная
- `develop` — рабочая

## Переменные окружения
Файлы `dev.env` и `prod.env` используются Docker'ом (см. docker-compose). Ключевые:
- `POSTGRES_USER` / `POSTGRES_PASSWORD` / `POSTGRES_DB` — настройки базы
- `DATABASE_URL` — формируется в docker-compose
- `ENVIRONMENT` — `local` или `production`
- `DJANGO_SECRET_KEY` — секретный ключ Django

> `prod.env` в `.gitignore`. На сервере создаётся вручную.

## Локальный запуск (без Docker)
Backend:
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r myproject/requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver 8000
```

Frontend:
```bash
cd frontend
npm install
npm run dev
```
Dev‑сервер Vite проксирует вызовы `/api/*` на `http://localhost:8000` (см. `vite.config.js`), удаляя префикс `/api`.

Открыть: `http://localhost:5173` (порт Vite может отличаться; по умолчанию в Vite 5173). Если нужны жёсткие порты – задайте через `VITE_DEV_SERVER_PORT`.

## Запуск через Docker

### Разработка
```bash
docker compose --env-file dev.env up -d --build
```

### Production (на сервере)
```bash
docker compose -f docker-compose.prod.yml --env-file prod.env up -d --build
```

Production запускает 3 контейнера:
- `school-db` — PostgreSQL 16
- `school-backend` — Django + Gunicorn (2 workers)
- `school-nginx` — Nginx (reverse proxy + SPA)

Доступы:
- Сайт: http://info-project.site
- Admin: http://info-project.site/admin/
- GraphQL: http://info-project.site/graphql/

## Сборка фронтенда для production
```bash
cd frontend
npm run build
```
Файлы собираются в `frontend/dist/` и **коммитятся в git** (на VPS недостаточно RAM для npm build).

## Загрузка seed-данных
```bash
# Локально
python manage.py seed_data

# На сервере
docker exec -it school-backend python manage.py seed_data

# С очисткой старых данных
docker exec -it school-backend python manage.py seed_data --clear
```

Данные загружаются из `myapp/management/commands/seed_data.json` (реальные данные МАОУ Гимназия №39).

## GraphQL
Схема расположена в `myapp/schema.py`. Эндпоинт: `/graphql/`.
## Деплой на VPS

SSH-доступ к серверу (см. `docs/ssh-deploy.md`):
```powershell
. .\scripts\vps-env.ps1
.\scripts\ssh-vps.ps1 "cd /opt/school-site && git pull origin develop && docker compose -f docker-compose.prod.yml --env-file prod.env up -d --build"
```

## Тестирование
```bash
python manage.py test
```

## Безопасность
- `SECRET_KEY` вынесен в переменные окружения
- `prod.env` в `.gitignore`
- `DEBUG=False` в production
- SSH-аутентификация по ключу

## Статус
Сайт задеплоен и работает на Jino VPS.
