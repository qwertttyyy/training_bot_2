
from src.bot.services.api.base import BaseAPIService
from src.bot.services.api.entities import Sportsman


class APIService(BaseAPIService):
    async def get_sportsman(self, chat_id):
        endpoint_urn = f"sportsmans/{chat_id}/"
        response = await self._get_request(endpoint_urn)
        if response.status_code == HTTPStatus.NOT_FOUND:
            return None
        return Sportsman(**response.json())
