import asyncio
import copy
import json
import locale
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
from src.bot.utils.configs import SHEET_DATE_FORMAT
from src.bot.utils.utils import get_formatted_date


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

    async def _read_values(self, sheet_range: str) -> list:
        response = await self._aiogoogle.as_service_account(
            self._service.spreadsheets.values.get(
                spreadsheetId=self._SPREADSHEET_ID, range=sheet_range
            )
        )
        return response.get("values")

    async def _write_values(self, sheet_range: str, values: list) -> None:
        body = {"majorDimension": "ROWS", "values": [values]}
        await self._aiogoogle.as_service_account(
            self._service.spreadsheets.values.update(
                spreadsheetId=self._SPREADSHEET_ID,
                range=sheet_range,
                valueInputOption="USER_ENTERED",
                json=body,
            )
        )

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

        date = datetime.today()
        locale.setlocale(locale.LC_ALL, "")
        for item in data[1:]:
            item["values"][0]["userEnteredValue"] = {
                "stringValue": get_formatted_date(SHEET_DATE_FORMAT, date)
            }
            date += timedelta(days=1)

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
            else:
                raise error

    async def send_data_to_sheet(
        self, full_name: str, column: str, values: list
    ):
        sheet_dates = await self._read_values(full_name + "!A2:A")
        sheet_dates = [date[0] if date else date for date in sheet_dates]
        locale.setlocale(locale.LC_ALL, "")
        row_index = sheet_dates.index(get_formatted_date(SHEET_DATE_FORMAT))
        await self._write_values(
            f"{full_name}!{column}{row_index + 2}", values
        )


async def main():
    async with GoogleSheetsService() as service:
        # await service.send_data_to_sheet("Михаил Морозов", "B", [7, 8, 60])
        # a = await service._read_values("Михаил Морозов!A2:A")
        # await service._write_values("Михаил Морозов!B2:D2", [1, 2, 3])
        await service.create_sportsman_sheets("Михаил", 12, 13)
        print(1)


if __name__ == "__main__":
    asyncio.run(main())
