from typing import List, Optional

from pydantic import BaseModel


class ClickUpTagItem(BaseModel):
    name: str


class ClickUpTaskItem(BaseModel):
    id: str
    name: str
    status: str
    assigned_name: str
    assigned_id: int
    tags: List[ClickUpTagItem]
    priority: str
    url: str
    time_estimate: Optional[int]
    points: Optional[int]
    folder_name: str
    list_name: str


class ClickUpUserData(BaseModel):
    id: int
    username: str
    email: str
    auth_token: str


class ClickUpTasks(BaseModel):
    tasks: List[ClickUpTaskItem]


class TeamData(BaseModel):
    id: int
    name: str
