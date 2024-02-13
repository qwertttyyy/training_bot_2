import os

from src.bot.utils.configs import BASE_DIR

INFO = {
    "type": os.getenv("TYPE"),
    "project_id": os.getenv("PROJECT_ID"),
    "private_key_id": os.getenv("PRIVATE_KEY_ID"),
    "private_key": os.getenv("PRIVATE_KEY"),
    "client_email": os.getenv("CLIENT_EMAIL"),
    "client_id": os.getenv("CLIENT_ID"),
    "auth_uri": os.getenv("AUTH_URI"),
    "token_uri": os.getenv("TOKEN_URI"),
    "auth_provider_x509_cert_url": os.getenv("AUTH_PROVIDER_X509_CERT_URL"),
    "client_x509_cert_url": os.getenv("CLIENT_X509_CERT_URL"),
}
SPREADSHEET_ID = os.getenv("SPREADSHEET_ID")
SHEET_STYLES_DIR = BASE_DIR / "google" / "styles"

SHEET_COLUMN_COUNT = 15
SHEET_ROW_COUNT = 1000
TABLE_COLUMN_COUNT = 9
TABLE_ROW_COUNT = 15
