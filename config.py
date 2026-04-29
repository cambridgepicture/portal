import os
from pathlib import Path

from dotenv import load_dotenv


BASE_PATH = Path(__file__).resolve().parent
load_dotenv(BASE_PATH / '.env')


BASE_DIR = str(BASE_PATH)
SECRET_KEY = os.getenv('SECRET_KEY', 'change-me-in-production')
STATIC_URL_PATH = '/static'
USER_DB_PATH = str(BASE_PATH / 'data' / '.user_store.sqlite3')
TRANSLATE_APP_URL = os.getenv('TRANSLATE_APP_URL', 'https://app.cambridgepicture.com/translate/')
LOGIN_USERNAME = os.getenv('LOGIN_USERNAME', 'ivan@cambridgepicture.com')
LOGIN_PASSWORD = os.getenv('LOGIN_PASSWORD', 'replace-with-your-password')
