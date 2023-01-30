import os
from dotenv import load_dotenv
load_dotenv()

RABBIT_HOST = os.environ.get("RABBIT_HOST") or "localhost"
LOGGER_LEVEL = os.environ.get("LOGGER_LEVEL") or "INFO"
LOGGER_FILE_PATH = os.environ.get("LOGGER_FILE_PATH") or "default_log.log"