import os
from pathlib import Path

from dotenv import load_dotenv


BASE_PATH = Path(__file__).resolve().parent
load_dotenv(BASE_PATH / '.env')


BASE_DIR = str(BASE_PATH)
SECRET_KEY = os.getenv('SECRET_KEY', 'change-me-in-production')
STATIC_URL_PATH = '/static'
USER_DB_PATH = str(BASE_PATH / 'data' / '.user_store.sqlite3')
LOGIN_USERNAME = os.getenv('LOGIN_USERNAME', 'admin')
LOGIN_PASSWORD = os.getenv('LOGIN_PASSWORD', 'admin')
