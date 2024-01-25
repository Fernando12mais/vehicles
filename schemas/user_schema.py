from typing import Optional
from pydantic import BaseModel


class CreateUserSchema(BaseModel):
    name: str
    password: str
