# Используем официальный образ Python
FROM python:3.9-slim

RUN apt-get update && apt-get install -y sqlite3
RUN pip install sqlfluff

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы зависимостей
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь код приложения
COPY . .

# Открываем порт для приложения
EXPOSE 5000

# Команда для запуска приложения
CMD ["python", "app.py"]
