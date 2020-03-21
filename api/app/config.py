from starlette.config import Config
from starlette.datastructures import Secret

config = Config("../.env")

DEBUG = config('DEBUG', cast=bool, default=False)
ALLOWED_ORIGINS = config(
    'ALLOWED_ORIGINS', default='*')
SECRET_KEY = config('SECRET_KEY', cast=Secret, default='test_secret')
LOCAL_PORT = config('LOCAL_PORT', default=8022)
DATASET_FILE_PATH = config('DATASET_FILE_PATH')
USERS_DB_FILE_PATH = config('USERS_DB_FILE_PATH')
DEFAULT_PAGE_LIMIT = 100
