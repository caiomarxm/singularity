from datetime import datetime
from pydantic import BaseModel, field_validator
from typing import Literal


class OAuth2AccessTokenEncoded(BaseModel):
    access_token: str
    token_type: Literal["bearer", "basic"] = "bearer"


class Oauth2AccessTokenContent(BaseModel):
    sub: str
    email: str
    exp: datetime

    @field_validator("sub", mode="before")
    @classmethod
    def convert_sub_to_str(cls, sub: int | str) -> str:
        if isinstance(sub, int):
            return str(sub)
        return sub
