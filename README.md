# ITNavigator

Объединённый интернет-каталог IT-решений на Django + Bootstrap + Docker

---

## Запуск с Docker

1. Убедитесь, что на вашей машине установлены [Docker](https://www.docker.com/)  
2. В корне проекта выполните:
```bash
   docker-compose up --build
```

3. Подождите, пока сервисы поднимутся, и откройте в браузере
   👉 [http://localhost:8000](http://localhost:8000)

Всё готово!

---

## Запуск без Docker

### 1. Клонировать репозиторий

```bash
git clone <REPO_URL>
cd ITNavigator
```

### 2. Создать и активировать виртуальное окружение

```bash
python3 -m venv .venv
# Linux / macOS
source .venv/bin/activate
# Windows (PowerShell)
.venv\Scripts\Activate.ps1
```

### 3. Установить зависимости

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Настроить базу данных

В `ITNavigator/settings.py`:

* **Закомментируйте** секцию с PostgreSQL:

  ```python
  # DATABASES = {
  #     "default": {
  #         "ENGINE": "django.db.backends.postgresql",
  #         "NAME": os.getenv("DB_NAME", "itnavigator_db"),
  #         ...
  #     }
  # }
  ```
* **Раскомментируйте** или вставьте секцию для SQLite:

  ```python
  DATABASES = {
      "default": {
          "ENGINE": "django.db.backends.sqlite3",
          "NAME": BASE_DIR / "db.sqlite3",
      }
  }
  ```

### 5. Миграции и начальные данные

1. Создайте таблицы:

   ```bash
   python manage.py migrate
   ```

2. Загрузите преднастроенные данные (если есть файлы фикстур):

   ```bash
   python manage.py loaddata data.json
   ```


### 6. Запуск локального сервера

```bash
python manage.py runserver
```

Перейдите в браузере по адресу 👉 [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## Структура проекта

```
.
├── catalog/               # Приложение с IT-решениями и запросами
│   ├── forms.py           # ModelForm-ы для ITSolution и ITRequest
│   ├── models.py          # Tag, ITSolution, ITRequest
│   ├── views.py           # solutions, solution_create, requests, request_create
│   ├── urls.py            # маршруты solutions/, requests/, .../create/
│   └── templates/…        # шаблоны catalog_solutions.html, catalog_requests.html
├── main/                  # Основное приложение (главная страница, аутентификация)
├── ITNavigator/           # Настройки Django (settings.py, urls.py, wsgi.py)
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── catalog.json           # Фикстуры для предварительного наполнения БД
└── manage.py
```

---
можно не регестрироваться а использовать готовые аккаунты для тестирования

Аккаут для Заказчика
init@gmail.com
12345678rt

Аккаунт для Компании
company2@gmail.com
12345678rt

Аккаут для superuser, admin
admin@gmail.com
12345678qw


Общийй функционал:
Посмотреть запросы или решения, предложить их, и можно одобрить или отклонить по  [admin-панель](http://127.0.0.1:8000/admin)


