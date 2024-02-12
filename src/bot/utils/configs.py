import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR.parent / ".data"

TOKEN = os.getenv("TOKEN")
