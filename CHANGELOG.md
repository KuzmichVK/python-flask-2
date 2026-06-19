# CHANGELOG — YaCut

Проверочная работа: REST API сервиса укорачивания ссылок.
Заполнены помеченные места заготовки.

## Структура (внимание на вложенность)

- git-корень репозитория: `python-flask-2/` (форк `KuzmichVK/python-flask-2`, ветка `main`).
- корень проекта (где `requirements.txt`, `settings.py`, пакет): `python-flask-2/yacut/`.
- пакет приложения: `python-flask-2/yacut/yacut/`.

Все dev-команды (`uv`, `flask`, `pytest`) — из корня проекта `python-flask-2/yacut/`.
git-команды работают оттуда же (git сам находит `.git` уровнем выше).

## Стек (как в requirements.txt — не менять)

flask==2.0.2, flask-sqlalchemy==2.5.1, sqlalchemy==1.4.29, flask-wtf==1.0.0,
wtforms==3.0.1, flask-migrate==3.1.0, python-dotenv==0.19.2, pytest==7.1.1.
Целевой Python: **3.10** (greenlet 1.1.2 не собирается на 3.11+).

## Изменения по файлам

### yacut/models.py
- Модель `URLMap`: поля id, original (String 1024), short (String 16, unique),
  timestamp (DateTime). Имена взяты из закомментированной заготовки и из кода
  view-функций (`URLMap(original=..., short=...)`, `filter_by(short=...)`).

### yacut/views.py
- `get_short_id()`: 6 случайных символов из `ascii_letters + digits`
  (длина = `ID_LENGHT` из `__init__.py`).
- `get_unique_short_id()`: генерирует, пока идентификатор не уникален.
- `index()` и `redirect_url()` оставлены как в заготовке (не трогал).

### yacut/api_views.py
- `create_id()` (POST `/api/id/`): валидация по openapi — нет тела →
  «Отсутствует тело запроса»; нет `url` → `"url" является обязательным полем!`;
  недопустимый `custom_id` → «Указано недопустимое имя для короткой ссылки»;
  занятый `custom_id` → `Имя "<id>" уже занято.`. Иначе создаёт запись и
  возвращает `{url, short_link}` + 201.
- `get_url()` (GET `/api/id/<short_id>/`): отдаёт `{url}` + 200; если не найдено
  — `InvalidAPIUsage('Указанный id не найден', 404)`.

### yacut/error_handlers.py
- Реализован класс `InvalidAPIUsage` (status_code по умолчанию 400,
  `to_dict()`); тело из закомментированной заготовки. Хэндлеры 404/500/
  InvalidAPIUsage — как в заготовке.

### .env (создан, корень проекта)
- FLASK_APP=yacut, FLASK_ENV=development, SECRET_KEY, DB=sqlite:///db.sqlite3.

### .gitignore (создан, git-корень — в репо его не было)
- .venv/venv, __pycache__, кэши, .env, *.sqlite3, migrations/, .DS_Store.

## Файлы без изменений (заготовка уже полная)

- `settings.py` (Config с дефолтами для DB и SECRET_KEY);
- `yacut/__init__.py` (app, db, migrate, ID_LENGHT=6, импорт api_views/views);
- `yacut/forms.py` (LinkForm: original_link + custom_id с Regexp/Optional/Length).

## Развёртывание (из python-flask-2/yacut/)

```bash
uv venv --python 3.10
uv pip install -r requirements.txt
```

## Создание таблицы БД

Надёжно (как делали на FitTrack), минуя `flask db`:

```bash
uv run python -c "from dotenv import load_dotenv; load_dotenv(); from yacut import app, db; ctx=app.app_context(); ctx.push(); db.create_all(); print('OK: таблица создана')"
```

Либо штатный миграционный путь, если `flask db` доступен:

```bash
uv run flask db init
uv run flask db migrate -m "url_map"
uv run flask db upgrade
```

## Прогон тестов (когда появится папка tests/)

```bash
uv run pytest tests/test_config.py
uv run pytest tests/test_database.py
uv run pytest tests/test_views.py
uv run pytest tests/test_endpoints.py
uv run pytest
```

## Запуск приложения

```bash
uv run flask run
```
