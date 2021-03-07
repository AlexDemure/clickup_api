import os

from pydantic import BaseSettings


class ClickUpSettings(BaseSettings):

    CLICKUP_CLIENT_ID: str = os.environ['CLICKUP_CLIENT_ID']
    CLICKUP_SECRET_KEY: str = os.environ['CLICKUP_SECRET_KEY']


click_up_settings = ClickUpSettings()
