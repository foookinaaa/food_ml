# Model Service Api

Example The ML service is a web application that provides an API for interacting with a machine learning model. It allows users to send queries with prediction data and get results back.

**Startup logic:**

When launched, the application initializes FastAPI, which handles HTTP requests. The app also connects to the machine learning model and loads it into memory for use in making predictions.

```
.
├── Dockerfile              # Файл Dockerfile для создания образа контейнера
├── pyproject.toml              # Файл с зависимостями и настройками проекта
├── docker-compose.yml          # Файл для управления контейнерами Docker
└── src
    ├── app.py                  # Основной файл приложения, инициализация FastAPI
    ├── api                     # Пакет с API роутами
    │   ├── __init__.py         # Инициализация пакета
    │   ├── routes              # Пакет с маршрутами API
    │   │   ├── __init__.py     # Инициализация пакета маршрутов
    │   │   ├── healthcheck.py  # Роут для проверки состояния сервиса
    │   │   ├── predict.py      # Роут для предсказаний модели
    │   │   └── router.py       # Основной маршрутизатор
    ├── schemas                  # Пакет с моделями данных
    │   ├── __init__.py         # Инициализация пакета
    │   ├── healthcheck.py      # Модель для ответов состояния сервиса
    │   └── requests.py         # Модель для входных запросов к API
    └── services                # Пакет с бизнес-логикой
        ├── __init__.py         # Инициализация пакета
        ├── model.py            # Логика работы с моделью машинного обучения
        └── utils.py            # Вспомогательные утилиты
```

## Getting started
local test:
```commandline
export PYTHONPATH='src'
poetry run uvicorn src.fast_api.app:app --host 0.0.0.0 --port 8000
```
http://127.0.0.1:8000/docs

```
docker-compose --project-directory src/fast_api/. up --build
```
web-server on
```
http://0.0.0.0:7007
```
swagger ui on
```
http://0.0.0.0:7007/docs
```
For test
```
curl -X 'POST' \
  'http://0.0.0.0:7007/api/predict/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
        "tree_dbh": 22,
        "curb_loc": 1,
        "steward": 0,
        "guards": 0,
        "sidewalk": 1,
        "problems": 1,
        "root_stone": 0,
        "root_grate": 0,
        "root_other": 0,
        "trunk_wire": 0,
        "trnk_light": 0,
        "trnk_other": 0,
        "brch_light": 1,
        "brch_shoe": 0,
        "brch_other": 0,
        "spc_common": "green ash",
        "zip_city": "Ozone Park",
        "borough": "Queens",
        "user_type": "NYC Parks Staff"
    }'
```
Answer on test:
```
{"Poor":0.0189,"Fair":0.1347,"Good":0.8464}
```

With celery:
```
model_service_api
├─ .docker
│  ├─ api.Dockerfile
│  └─ worker.Dockerfile
├─ docker-compose.yml
├─ poetry.lock
├─ pyproject.toml
└─ src
   ├─ api
   │  ├─ __init__.py
   │  └─ routes
   │     ├─ __init__.py
   │     ├─ healthcheck.py
   │     ├─ predict.py
   │     └─ router.py
   ├─ app.py
   ├─ connections
   │  └─ broker.py
   ├─ models
   │  ├─ __init__.py
   │  ├─ healthcheck.py
   │  └─ requests.py
   ├─ services
   │  ├─ __init__.py
   │  ├─ model.py
   │  └─ utils.py
   └─ worker
      └─ predict_worker.py

```
```commandline
docker-compose --project-directory src/fast_api/. down
```
