from urllib.parse import urljoin

from httpx import AsyncClient, Response

from src.bot.utils.configs import INTERNAL_API_URL


class BaseAPIService:
    BASE_URL = INTERNAL_API_URL

    async def _get_request(self, endpoint_urn: str) -> Response:
        async with AsyncClient() as client:
            response = await client.get(urljoin(self.BASE_URL, endpoint_urn))
        return response

    async def _post_request(self, endpoint_urn: str, data: dict) -> Response:
        async with AsyncClient() as client:
            response = await client.post(
                urljoin(self.BASE_URL, endpoint_urn), data=data
            )
            response.raise_for_status()
        return response

    async def _patch_request(self, endpoint_urn: str, data: dict) -> Response:
        async with AsyncClient() as client:
            response = await client.patch(
                urljoin(self.BASE_URL, endpoint_urn), data=data
            )
            response.raise_for_status()
        return response

    async def _delete_request(self, endpoint_urn: str) -> Response:
        async with AsyncClient() as client:
            response = await client.delete(
                urljoin(self.BASE_URL, endpoint_urn)
            )
            response.raise_for_status()
        return response
