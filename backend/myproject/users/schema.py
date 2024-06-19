from pydantic import BaseModel


class UserInput(BaseModel):
    email: str
    password: str
    