from starlette.config import Config
from starlette.datastructures import Secret

config = Config("../.env")

DEBUG = config('DEBUG', cast=bool, default=False)
ALLOWED_ORIGINS = config(
    'ALLOWED_ORIGINS', default='*')
SECRET_KEY = config('SECRET_KEY', cast=Secret, default='test_secret')
LOCAL_PORT = config('PORT', default=8000)
DATASET_FILE_PATH = config('DATASET_FILE_PATH')
DEFAULT_PAGE_LIMIT = config('DEFAULT_PAGE_LIMIT', cast=int, default=1000)
