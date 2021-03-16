from io import BufferedReader
from common.base_class import APIClass
from oauth.service import OAuth, OAuthUtils
from .enums import ClickUpTaskStatusType
from .schemas import ClickUpTasks, ClickUpCreateTask
from .serializer import prepare_task
from .settings import click_up_settings


class Users(APIClass):

    async def get_user_by_token(self) -> dict:
        """Получение пользовательских данных"""
        url = 'https://api.clickup.com/api/v2/user'  # Получение данных о пользователе по токену.

        r_json = await self.make_request("GET", url)
        return r_json['user']

    async def get_user_by_team_id_and_user_id(self, team_id: int, user_id: int) -> dict:
        """
        Получение пользовательских данных.

        Только для команд с Enterprise статусом. Без него будет возвращаться 403.
        """
        url = f'https://api.clickup.com/api/v2/team/{team_id}/user/{user_id}'

        r_json = await self.make_request("GET", url)
        return r_json['member']['user']

    async def get_users_by_task(self, task_id: str) -> dict:
        """Получение пользовательских данных"""
        url = f'https://api.clickup.com/api/v2/task/{task_id}/member'

        r_json = await self.make_request("GET", url)
        return r_json['members']


class Teams(APIClass):

    async def get_teams(self) -> list:
        url = 'https://api.clickup.com/api/v2/team'  # Получение данных о пользователе по токену.

        r_json = await self.make_request("GET", url)
        return r_json['teams']


class Spaces(APIClass):

    async def get_spaces(self, team_id: int) -> list:
        url = f"https://api.clickup.com/api/v2/team/{team_id}/space?archived=false"
        r_json = await self.make_request("GET", url)
        return r_json['spaces']


class Folders(APIClass):

    async def get_folders(self, space_id: int) -> list:
        url = f"https://api.clickup.com/api/v2/space/{space_id}/folder?archived=false"
        r_json = await self.make_request("GET", url)
        return r_json['folders']

    async def get_folder(self, folder_id: int) -> list:
        url = f"https://api.clickup.com/api/v2/folder/{folder_id}"
        r_json = await self.make_request("GET", url)
        return r_json


class Lists(APIClass):

    async def get_lists(self, folder_id: int):
        url = f"https://api.clickup.com/api/v2/folder/{folder_id}/list?archived=false"
        r_json = await self.make_request("GET", url)
        return r_json['lists']


class Tasks(APIClass):

    async def get_tasks(self, team_id: int, click_user_id: int):
        url = f"https://api.clickup.com/api/v2/team/{team_id}/task?assignees%5B%5D={click_user_id}"

        r_json = await self.make_request("GET", url)
        return r_json['tasks']

    async def create_task(self, list_id: int, task: ClickUpCreateTask):
        url = f"https://api.clickup.com/api/v2/list/{list_id}/task/"
        r_json = await self.make_request("POST", url, task.dict())
        return r_json

    async def get_task(self, task_id: str):
        url = f"https://api.clickup.com/api/v2/task/{task_id}/"

        r_json = await self.make_request("GET", url)
        return r_json

    async def get_tasks_by_list(self, list_id: int):
        url = f"https://api.clickup.com/api/v2/list/{list_id}/task"

        r_json = await self.make_request("GET", url)
        return r_json['tasks']

    async def get_task_comments(self, task_id: str):
        url = f"https://api.clickup.com/api/v2/task/{task_id}/comment/"

        r_json = await self.make_request("GET", url)
        return r_json['comments']

    async def add_task_comment(self, task_id: str, payload: dict):
        url = f"https://api.clickup.com/api/v2/task/{task_id}/comment/"

        r_json = await self.make_request("POST", url, payload)
        return r_json

    async def add_task_attachment(self, task_id: str, file_io: BufferedReader):
        url = f'https://api.clickup.com/api/v2/task/{task_id}/attachment'
        files = [
            (
                'attachment',
                (
                    file_io.name,
                    file_io,
                    'application/octet-stream'
                )
            )
        ]

        r_json = await self.make_request_send_file(url, files)
        return r_json


class WebHooks(APIClass):

    async def create_webhook(self, team_id: int, endpoint: str):
        url = f"https://api.clickup.com/api/v2/team/{team_id}/webhook"

        # Endpoint - куда кликап будет отправлять запросы.
        # Events - список всех событий в clickup.
        payload = dict(endpoint=endpoint, events=["*"])

        r_json = await self.make_request("POST", url, payload)
        return r_json

    async def get_webhooks(self, team_id: int):
        url = f"https://api.clickup.com/api/v2/team/{team_id}/webhook"

        r_json = await self.make_request("GET", url)
        return r_json['webhooks']

    async def delete_webhook(self, webhook_id: str):
        url = f"https://api.clickup.com/api/v2/webhook/{webhook_id}"

        r_json = await self.make_request("DELETE", url)
        return r_json


class ClickUp(Users, Teams, Spaces, Folders, Lists, Tasks, WebHooks):
    """
    Класс для работы с ClickUP API.
    """

    async def collect_user_tasks(self, click_user_id: int = None) -> ClickUpTasks:
        """
        Метод по сбору назначенных задач на пользователя по всему WorkSpace.

        Данный метод определяет тот WorkSpace который был выбран при подключении ClickUp и собирает по нему данные.
        Данные собираются по всем областям перебирая каждую сущность: Spaces, Folders, Folders List, Tasks.
        Перебор происходит из-за архитектуры clickup которая деклалирует сбор данных по этапно.
        Чтобы добраться до Tasks необходимо произвести всю цепочку.
        WorkSpace -> Spaces (list) -> Folders (list) -> FoldersLists (lists) -> Tasks (lists)
        """
        teams = await self.get_teams()

        prepared_tasks = []
        for team in teams:
            tasks = await self.get_tasks(team['id'], click_user_id)
            prepared_tasks += [
                prepare_task(x) for x in tasks if x['folder']['name'] != "Backlog" and x['list']['name'] != "Backlog"
            ]

        return ClickUpTasks(tasks=prepared_tasks)

    async def collect_tasks(self, list_id: int, status_type: ClickUpTaskStatusType) -> ClickUpTasks:
        """
        Метод по сбору всех задач в списке.

        :param list_id ID-списка в проекте:
        :param status - тип статуса задачи. Могут быть 3 типа close, done, open
        """
        tasks = await self.get_tasks_by_list(list_id)

        if status_type == ClickUpTaskStatusType.done:
            # Если статус задачи является выполненным он переход в опрд. тип задач
            # который ClickUp выставляет автоматический в виде галочки.
            tasks = [prepare_task(x) for x in tasks if x['status']['type'] == status_type.value]

        else:
            # В другом случае отсортировываем все задачи у которых тип отличается от выполненного.
            tasks = [prepare_task(x) for x in tasks if x['status']['type'] != ClickUpTaskStatusType.done.value]

        return ClickUpTasks(tasks=tasks)


class ClickUpOAuth(OAuth):
    """Класс с полным процессом получения авторизационного токена для работы с ClickUp."""

    client_id = click_up_settings.CLICKUP_CLIENT_ID
    client_secret = click_up_settings.CLICKUP_SECRET_KEY

    @staticmethod
    def get_code_url(redirect_uri: str, state: dict) -> str:
        """Шаг №1 Получение ссылки с кодом подтверждения."""
        return f"https://app.clickup.com/api" \
               f"?client_id={click_up_settings.CLICKUP_CLIENT_ID}" \
               f"&state={OAuthUtils.encode_state_to_base64(state)}" \
               f"&redirect_uri={redirect_uri}"

    @classmethod
    def get_token_url(cls, code: str, redirect_uri: str = None):
        return f'https://api.clickup.com/api/v2/oauth/token?' \
              f'client_id={click_up_settings.CLICKUP_CLIENT_ID}&' \
              f'client_secret={click_up_settings.CLICKUP_SECRET_KEY}&' \
              f'code={code}'
