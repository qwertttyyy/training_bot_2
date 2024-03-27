from http import HTTPStatus

from src.bot.services.api.base import BaseAPIService
from src.bot.services.api.entities import Sportsman


class APIService(BaseAPIService):
    async def get_sportsman(self, chat_id):
        endpoint_urn = f"sportsmans/{chat_id}/"
        response = await self._get_request(endpoint_urn)
        if response.status_code == HTTPStatus.NOT_FOUND:
            return None
        return Sportsman(**response.json())

    async def get_sportsmans_list(self):
        endpoint_urn = f"sportsmans/"
        response = await self._get_request(endpoint_urn)
        return [Sportsman(**item) for item in response.json()]

    async def save_sportsman(
        self, chat_id, name, surname, sheet_id, archive_sheet_id
    ):
        sportsman_data = {
            "chat_id": chat_id,
            "name": name,
            "surname": surname,
            "sheet_id": sheet_id,
            "archive_sheet_id": archive_sheet_id,
        }
        endpoint_urn = f"sportsmans/"
        await self._post_request(endpoint_urn, sportsman_data)

    async def save_feeling(self, chat_id, rating, sleep_hours, heart_rate):
        endpoint_urn = "feelings/"
        feeling_data = {
            "chat_id": chat_id,
            "rating": rating,
            "sleep_hours": sleep_hours,
            "heart_rate": heart_rate,
        }
        await self._post_request(endpoint_urn, feeling_data)
