import json

import httpx


class APIClass:

    _session: httpx.AsyncClient = None

    _headers = None

    def __init__(self, access_token: str = None):
        self._headers: dict = {
            "Accept": "application/json",
            'Content-Type': 'application/json',
        }
        if access_token is not None:
            self._headers['Authorization'] = access_token

    @property
    def _client_session(self) -> httpx.AsyncClient:
        if not self._session or self._session.is_closed:
            self._session = httpx.AsyncClient(headers=self._headers)

        return self._session

    async def make_request(self, method: str, url: str, payload: dict = None):
        request = httpx.Request(method, url, headers=self._headers, json=payload)
        response = await self._client_session.send(request)

        return self._check_result(request, response)

    @staticmethod
    def _check_result(request: httpx.Request, response: httpx.Response):
        if response.status_code != 200:
            raise httpx.HTTPStatusError("Error status_code", request=request, response=response)

        try:
            return response.json()
        except json.decoder.JSONDecodeError:
            raise httpx.DecodingError("Error decode to json", request=request)
