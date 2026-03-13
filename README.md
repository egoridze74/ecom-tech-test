# ecom-tech-test
## Инструкция по запуску

```bash
# Клонировать репозиторий
git clone https://github.com/egoridze74/ecom-tech-test
cd ecom-tech-test

# Запустить через Docker
docker-compose up --build

# API доступно по http://localhost:8000
# Или можно тестировать при помощи curl в cmd:
curl -X POST "http://localhost:8000/upload-grades" -F "file=@test.csv"
curl "http://localhost:8000/students/more-than-3-twos"
curl "http://localhost:8000/students/less-than-5-twos"
```

## Структура проекта
```
ecom-tech-test/
├── app/
│   ├── __init__.py
│   ├── crud.py
│   ├── database.py
│   ├── main.py
│   ├── schemas.py
│   └── upload.py
├── sql_scripts/
│   └── create_grades.sql
├── docker-compose.yml
├── Dockerfile
├── README.md
└── requirements.txt
```