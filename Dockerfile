# Используем официальный Python-образ
FROM python:3.11-slim

# Устанавливаем переменные окружения:
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Создаём директорию для приложения и работаем внутри неё
WORKDIR /app

# Скопируем файл с зависимостями и установим их
COPY requirements.txt /app/
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# Скопируем всю директорию проекта (включая ITNavigator и manage.py) внутрь образа
COPY . /app/

# При запуске контейнера по умолчанию запустим команду, указанную в docker-compose.yml
# (обычно это сбор миграций и запуск dev-сервера). Здесь можно оставить ENTRYPOINT пустым.
