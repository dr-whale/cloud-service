import os
from dotenv import load_dotenv
#dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
#if os.path.exists(dotenv_path):
    #load_dotenv(dotenv_path)
load_dotenv()

API_KEY = os.environ.get("API_KEY")
BASE_URL = os.environ.get("BASE_URL") or 'https://api.weather.yandex.ru/v2'
DATA_URL = os.environ.get("DATA_URL") or '/informers'
PARAMS = os.environ.get("PARAMS") or {'lat': '59.9386', 'lon': '30.3141'}
RABBIT_HOST = os.environ.get("RABBIT_HOST") or 'localhost'
REDIS_HOST = os.environ.get("REDIS_HOST") or 'localhost'