import django
from django.conf import settings
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
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
