import json
from datetime import datetime, timedelta

import aiofiles
from aiogoogle import Aiogoogle
from aiogoogle.auth.creds import ServiceAccountCreds

from configs import (
    SPREADSHEET_ID,
    INFO,
    SHEET_STYLES_DIR,
    SHEET_ROW_COUNT,
    SHEET_COLUMN_COUNT,
    TABLE_COLUMN_COUNT,
    TABLE_ROW_COUNT,
)
from src.bot.utils.configs import DATE_FORMAT


class GoogleSheetsService:
    _SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
    _SPREADSHEET_ID = SPREADSHEET_ID
    _INFO = INFO
    _header_style_file = SHEET_STYLES_DIR / "header_style.json"
    _sheet_style_file = SHEET_STYLES_DIR / "sheet_style.json"
    _service = None
    _aiogoogle = None

    async def init_service(self):
        creds = ServiceAccountCreds(scopes=self._SCOPES, **self._INFO)
        async with Aiogoogle(service_account_creds=creds) as aiogoogle:
            self._aiogoogle = aiogoogle
            self._service = await aiogoogle.discover("sheets", "v4")

    async def _batch_update(self, body: dict):
        response = await self._aiogoogle.as_service_account(
            self._service.spreadsheets.batchUpdate(
                spreadsheetId=self._SPREADSHEET_ID, json=body
            )
        )
        return response

    @staticmethod
    async def _read_json_file(filepath: str) -> dict:
        async with aiofiles.open(filepath, mode="r", encoding="utf-8") as f:
            return json.loads(await f.read())

    async def _create_sheet(self, sheet_name) -> int:
        requests = [
            {
                "addSheet": {
                    "properties": {
                        "title": sheet_name,
                        "gridProperties": {
                            "rowCount": SHEET_ROW_COUNT,
                            "columnCount": SHEET_COLUMN_COUNT,
                        },
                    }
                }
            }
        ]
        response = await self._batch_update({"requests": requests})
        sheet_id = response["replies"][0]["addSheet"]["properties"]["sheetId"]
        return sheet_id

    async def create_sportsman_sheet(self, sheet_name: str) -> int:
        sheet_id = await self._create_sheet(sheet_name)
        styles = await self._read_json_file(self._sheet_style_file)
        data = styles["sheets"][0]["data"][0]["rowData"]

        today = datetime.today().date()
        for item in data[1:]:
            item["values"][0]["userEnteredValue"] = {
                "stringValue": today.strftime(DATE_FORMAT)
            }
            today += timedelta(days=1)

        requests = [
            {
                "updateCells": {
                    "rows": data,
                    "fields": "userEnteredValue.stringValue,"
                    "userEnteredFormat.numberFormat,"
                    "userEnteredFormat.borders,"
                    "userEnteredFormat.backgroundColor,"
                    "userEnteredFormat.horizontalAlignment,"
                    "userEnteredFormat.verticalAlignment,"
                    "userEnteredFormat.textFormat",
                    "range": {
                        "sheetId": sheet_id,
                        "startRowIndex": 0,
                        "startColumnIndex": 0,
                        "endRowIndex": TABLE_ROW_COUNT,
                        "endColumnIndex": TABLE_COLUMN_COUNT,
                    },
                }
            }
        ]

        await self._batch_update({"requests": requests})
        return sheet_id
