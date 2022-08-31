FROM python:3.9

# Сделать директорию /app рабочей директорией. 
WORKDIR /app

# Скопировать с локального компьютера файл зависимостей
# в директорию /app.
COPY requirements.txt .

RUN python -m pip install --upgrade pip
# Выполнить установку зависимостей внутри контейнера.
RUN pip install -r requirements.txt --no-cache-dir

COPY . .

RUN python manage.py collectstatic --no-input

LABEL author='Albrant Eugene' author_mail='skizee@yandex.ru'

# Выполнить запуск сервера разработки при старте контейнера.
# Это пригодится, если нужно поработать с базой данных
# CMD ["python3", "manage.py", "runserver", "0:8000"] 
# Выполнить запуск скрипта bot_manager.py
CMD ["python3", "bot_manager.py"] 
