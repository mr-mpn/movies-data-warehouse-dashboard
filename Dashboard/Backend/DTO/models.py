from pydantic import BaseModel

class UserSignUp(BaseModel):
    username: str
    password: str
