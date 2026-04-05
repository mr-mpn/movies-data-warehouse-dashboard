from pydantic import BaseModel

class AuthenticationRequest(BaseModel):
    username: str
    password: str

class AuthenticationResponse(BaseModel):
    message: str

class HomeResponse(BaseModel):
    title: str
    vote_average: float
    vote_count: float