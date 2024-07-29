from typing import Optional
from sqlmodel import SQLModel, Field


class User(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True)
    name: Optional[str]
    email: str
    hashed_password: str
