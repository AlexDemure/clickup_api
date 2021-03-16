from typing import List, Optional

from pydantic import BaseModel


class BaseData(BaseModel):
    id: int
    name: str


class MemberItem(BaseData):
    pass


class ListData(BaseData):
    pass


class FolderData(BaseData):
    lists: List[ListData]


class SpaceData(BaseData):
    folders: List[FolderData]


class TeamData(BaseData):
    spaces: List[SpaceData]


class ClickUpData(BaseModel):
    teams: List[TeamData]


class ClickUpTagItem(BaseModel):
    name: str


class ClickUpCreateTask(BaseModel):
    name: str
    description: str
    assignees: List
    tags: List
    status: str = "Open"
    priority: int


class ClickUpTaskItem(BaseModel):
    id: str
    name: str
    status: str
    assigned: List
    tags: List[ClickUpTagItem]
    priority: str
    url: str
    time_estimate: Optional[int]
    points: Optional[int]
    folder_name: str
    list_name: str


class ClickUpUser(BaseModel):
    id: int
    username: str
    email: str


class ClickUpUserData(ClickUpUser):
    """Схема для работы с токенами и ролями."""
    role: int
    auth_token: str


class ClickUpTasks(BaseModel):
    tasks: List[ClickUpTaskItem]


class UserGroups(BaseModel):
    owner: List[ClickUpUser]
    admin: List[ClickUpUser]
    member: List[ClickUpUser]
    guest: List[ClickUpUser]


