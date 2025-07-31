# WIKII. Сервис хранения объектов критической информационной инфраструктуры.

---

### Начало работы

Создание виртуального окружения:

```
python -m venv .venv
```

Его активация в случае Windows:

```
.\.venv\Scripts\activate
```

В случае Linux и MacOS:

```
source ./.venv/bin/activate
```

Загрузка зависимостей:

```
pip install -r requirements.txt
```

Применение миграций:

```
python manage.py migrate
```

Создание суперпользователя:

```
python manage.py createsuperuser
```

Запуск сервера:

```
python manage.py runserver 127.0.0.1:8000
```

---
