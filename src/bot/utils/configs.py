import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR.parent / ".data"

API_TOKEN = os.getenv("API_TOKEN")

TRAINER_ID = os.getenv("TRAINER_ID")

DATE_FORMAT = "%d.%m.%Y"

INTERNAL_API_URL = os.getenv(
    "INTERNAL_API_URL", "http://127.0.0.1:8000/api/v1/"
)
