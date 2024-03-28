from urllib.parse import urljoin

from httpx import AsyncClient, Response


class BaseAPIService:
    def __init__(self, base_url):
        self.base_url = base_url

    async def _get_request(self, endpoint_urn: str) -> Response:
        async with AsyncClient() as client:
            response = await client.get(urljoin(self.base_url, endpoint_urn))
        return response

    async def _post_request(self, endpoint_urn: str, data: dict) -> Response:
        async with AsyncClient() as client:
            response = await client.post(
                urljoin(self.base_url, endpoint_urn), data=data
            )
        return response

    async def _patch_request(self, endpoint_urn: str, data: dict) -> Response:
        async with AsyncClient() as client:
            response = await client.patch(
                urljoin(self.base_url, endpoint_urn), data=data
            )
        return response

    async def _delete_request(self, endpoint_urn: str) -> Response:
        async with AsyncClient() as client:
            response = await client.delete(
                urljoin(self.base_url, endpoint_urn)
            )
        return response
