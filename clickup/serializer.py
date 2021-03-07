from typing import List

from .enums import TagsEnumsByEmoji
from .schemas import ClickUpTaskItem, ClickUpTagItem, ClickUpUserData


def prepare_tags(tags: list) -> List[ClickUpTagItem]:
    prepared_tags = []
    for tag in tags:
        if getattr(TagsEnumsByEmoji, tag['name'], None):  # Отображаем лишь те теги которые есть у нас в Enums
            prepared_tags.append(ClickUpTagItem(name=tag['name']))

    return prepared_tags


def tags_list_to_emoji_str(tags: List[ClickUpTagItem]) -> str:
    """Преобразовывает список тегов в одну строку брав вместо названия тега его emoji."""
    tags_to_str = ""
    for tag in tags:
        try:
            tags_to_str += f"{TagsEnumsByEmoji(tag.name).emoji}"
        except ValueError:
            continue

    return tags_to_str


def prepare_task(task: dict) -> ClickUpTaskItem:

    return ClickUpTaskItem(
        id=task['id'],
        name=task['name'],
        status=task['status']['status'],
        assigned_name=task['assignees'][0]['username'] if task['assignees'] else "NOT_SET",
        assigned_id=task['assignees'][0]['id'] if task['assignees'] else "NOT_SET",
        tags=prepare_tags(task['tags']) if task['tags'] else [],
        priority=task['priority']['priority'] if task['priority'] else "NOT_SET",
        url=task['url'],
        time_estimate=task['time_estimate'] if task['time_estimate'] else None,
        points=task['points'] if task['points'] else None,
        folder_name=task['folder']['name'],
        list_name=task['list']['name'],

    )


def prepare_user_data(user_data: dict, token_data: dict) -> ClickUpUserData:
    return ClickUpUserData(
        id=user_data['id'],
        username=user_data['username'],
        email=user_data['email'],
        auth_token=token_data['access_token'],  # Type Bearer ставить не надо.
    )

