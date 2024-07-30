from pydantic import BaseModel

from singularity.authentication.oauth2.models import OAuth2AccessTokenEncoded


class LoginRequestData(BaseModel):
    username: str
    password: str


class LoginResponseData(OAuth2AccessTokenEncoded):
    pass
