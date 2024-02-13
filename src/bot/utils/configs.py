import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR.parent / ".data"

TOKEN = os.getenv("TOKEN")

TRAINER_ID = os.getenv("TRAINER_ID")

DATE_FORMAT = "%d.%m.%Y"
