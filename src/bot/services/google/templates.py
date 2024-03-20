from src.bot.services.google.configs import (
    SHEET_ROW_COUNT,
    SHEET_COLUMN_COUNT,
    TABLE_ROW_COUNT,
    TABLE_COLUMN_COUNT,
)

ADD_SHEET_REQUEST = {
    "addSheet": {
        "properties": {
            "title": "Default",
            "sheetId": int,
            "gridProperties": {
                "rowCount": SHEET_ROW_COUNT,
                "columnCount": SHEET_COLUMN_COUNT,
            },
        }
    }
}

UPDATE_CELLS_REQUEST = {
    "updateCells": {
        "rows": list,
        "fields": "userEnteredValue.stringValue,"
        "userEnteredFormat.numberFormat,"
        "userEnteredFormat.borders,"
        "userEnteredFormat.backgroundColor,"
        "userEnteredFormat.horizontalAlignment,"
        "userEnteredFormat.verticalAlignment,"
        "userEnteredFormat.textFormat",
        "range": {
            "sheetId": int,
            "startRowIndex": 0,
            "startColumnIndex": 0,
            "endRowIndex": TABLE_ROW_COUNT,
            "endColumnIndex": TABLE_COLUMN_COUNT,
        },
    }
}
