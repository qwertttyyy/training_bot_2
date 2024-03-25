import copy
import json
from datetime import datetime, timedelta

import aiofiles
from aiogoogle import Aiogoogle
from aiogoogle.auth.creds import ServiceAccountCreds
from aiogoogle.excs import HTTPError

from src.bot.services.google.configs import (
    SPREADSHEET_ID,
    INFO,
    SHEET_STYLES_DIR,
)
from src.bot.services.google.templates import (
    ADD_SHEET_REQUEST,
    UPDATE_CELLS_REQUEST,
)
from src.bot.utils.configs import DATE_FORMAT


class GoogleSheetsService:
    _SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
    _SPREADSHEET_ID = SPREADSHEET_ID
    _INFO = INFO
    _header_style_file = SHEET_STYLES_DIR / "header_style.json"
    _sheet_style_file = SHEET_STYLES_DIR / "sheet_style.json"

    async def __aenter__(self):
        creds = ServiceAccountCreds(scopes=self._SCOPES, **self._INFO)
        self._aiogoogle = Aiogoogle(service_account_creds=creds)
        self._service = await self._aiogoogle.discover("sheets", "v4")
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self._aiogoogle:
            await self._aiogoogle.__aexit__(exc_type, exc_val, exc_tb)

    async def _batch_update(self, body: list):
        body = {"requests": body}
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

    @staticmethod
    async def _add_create_sheet_request(
        sheet_name: str, sheet_id: int, requests: list
    ):
        request = copy.deepcopy(ADD_SHEET_REQUEST)
        request["addSheet"]["properties"]["sheetId"] = sheet_id
        request["addSheet"]["properties"]["title"] = sheet_name
        requests.append(request)

    @staticmethod
    async def _add_update_sheet_request(
        sheet_id: int, rows: list, requests: list
    ):
        request = copy.deepcopy(UPDATE_CELLS_REQUEST)
        request["updateCells"]["rows"] = rows
        request["updateCells"]["range"]["sheetId"] = sheet_id
        requests.append(request)

    async def create_sportsman_sheets(
        self, sheet_name: str, sheet_id: int, archive_sheet_id: int
    ):
        requests = []
        await self._add_create_sheet_request(sheet_name, sheet_id, requests)
        await self._add_create_sheet_request(
            f"{sheet_name}_АРХИВ", archive_sheet_id, requests
        )
        styles = await self._read_json_file(self._sheet_style_file)
        data = styles["sheets"][0]["data"][0]["rowData"]

        today = datetime.today().date()
        for item in data[1:]:
            item["values"][0]["userEnteredValue"] = {
                "stringValue": f"{today:{DATE_FORMAT}}"
            }
            today += timedelta(days=1)

        await self._add_update_sheet_request(sheet_id, data, requests)

        header = await self._read_json_file(self._header_style_file)
        await self._add_update_sheet_request(
            archive_sheet_id, [header], requests
        )
        try:
            await self._batch_update(requests)
        except HTTPError as error:
            if "already exists" in error.res.error_msg:
                print(f"Лист с именем {sheet_name} уже существует")
