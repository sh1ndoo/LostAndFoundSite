# Используем официальный образ Python
FROM python:3.11-slim

# Устанавливаем переменные окружения
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файл с зависимостями и устанавливаем их
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь проект в рабочую директорию
COPY . .

# Собираем статические файлы
# STATIC_ROOT должен быть определен в settings.py
RUN python manage.py collectstatic --noinput

# Открываем порт, на котором будет работать Gunicorn
EXPOSE 8000

# Запускаем Gunicorn. 'config.wsgi' - это путь к вашему wsgi-файлу.
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "config.wsgi:application"]
