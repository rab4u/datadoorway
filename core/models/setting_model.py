from pydantic.main import BaseModel


class SettingModel(BaseModel):
    key: str
    value: str | list | set | dict
