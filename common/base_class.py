import json

import httpx
from tenacity import retry, wait_fixed, stop_after_attempt


class APIClass:

    _headers = None

    def __init__(self, access_token: str = None):
        self._headers: dict = {
            "Accept": "application/json",
            'Content-Type': 'application/json',
        }
        if access_token is not None:
            self._headers['Authorization'] = access_token

    @retry(
        wait=wait_fixed(1),
        stop=stop_after_attempt(3),
        reraise=True
    )
    async def make_request(self, method: str, url: str, payload: dict = None):
        request = httpx.Request(method, url, headers=self._headers, json=payload)
        async with httpx.AsyncClient(headers=self._headers) as session:
            response = await session.send(request)
            return self._check_result(request, response)

    async def make_request_send_file(self, url, files):
        self._headers.pop("Content-Type", None)

        request = httpx.Request("POST", url, headers=self._headers, files=files)
        async with httpx.AsyncClient(headers=self._headers) as session:
            response = await session.send(request)
            return self._check_result(request, response)

    @staticmethod
    def _check_result(request: httpx.Request, response: httpx.Response):
        if response.status_code != 200:
            raise httpx.HTTPStatusError("Error status_code", request=request, response=response)

        try:
            return response.json()
        except json.decoder.JSONDecodeError:
            raise httpx.DecodingError("Error decode to json", request=request)
