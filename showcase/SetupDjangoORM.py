import os
from pathlib import Path

import django
from django.conf import settings
from dotenv import load_dotenv

# загружаем секретные данные из .env
load_dotenv()
VK_API_TOKEN = os.getenv('VK_API_TOKEN')
ID_PUBLIC = os.getenv('ID_PUBLIC')

# производим настройки Django ORM, чтобы можно было работать
# с базой данных без запуска основного скрипта Django
BASE_DIR = Path(__file__).resolve().parent
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# количество строк в клавиатуре ВК
KEYBOARD_ROWS = 10

settings.configure(
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
        },
    INSTALLED_APPS=[
        'backend',
    ]
)

django.setup()
