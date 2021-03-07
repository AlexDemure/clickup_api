from .utils import encode_str_to_base64, encode_dict_to_base64

from common.base_class import APIClass


class OAuth(APIClass):

    client_id = None
    client_secret = None

    @staticmethod
    def get_code_url(redirect_uri: str, state: dict):
        """Шаг №1 Получение ссылки с кодом подтверждения."""
        raise NotImplementedError

    @staticmethod
    def get_token_url(code: str, redirect_uri: str = None):
        """
        Шаг №2.1 Получение ссылки с применением code для получения авторизационного токена.

        Этот шаг наступает после пользовательской авторизации на сайте и получения уведомления об успешной авторизации.
        """
        raise NotImplementedError

    async def get_token(self, code: str, redirect_uri: str = None, is_basic_token: bool = False) -> dict:
        """
        Шаг №2.2 Отправка запроса на получение авторизационного токена
        """
        if is_basic_token:
            access_basic_token = f"Basic {OAuthUtils.get_basic_token_to_base64(self.client_id, self.client_secret)}"
            self._headers['Authorization'] = access_basic_token

        url = self.get_token_url(code, redirect_uri)
        return await self.make_request("POST", url)


class OAuthUtils:

    @staticmethod
    def get_basic_token_to_base64(client_id: str, client_secret: str) -> str:
        """
        Шифрование Basic токена.

        В некоторых сервисах требуют в Headers отправлять Basic токен с данными клиента.
        """
        return encode_str_to_base64(f"{client_id}:{client_secret}")

    @staticmethod
    def encode_state_to_base64(state: dict) -> str:
        return encode_dict_to_base64(state)
