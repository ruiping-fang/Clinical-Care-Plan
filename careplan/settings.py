import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'dev-secret-key'
DEBUG = True
ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.staticfiles',
    'app',
]

MIDDLEWARE = []

ROOT_URLCONF = 'careplan.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'app/templates'],
        'APP_DIRS': True,
        'OPTIONS': {},
    },
]

STATIC_URL = '/static/'

# OpenAI Key
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")