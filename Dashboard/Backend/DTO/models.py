from pydantic import BaseModel
from typing import List

class AuthenticationRequest(BaseModel):
    username: str
    password: str

class AuthenticationResponse(BaseModel):
    message: str

class HomeResponse(BaseModel):
    id: int
    title: str
    vote_average: float
    vote_count: int

class PaginatedHomeResponse(BaseModel):
    movies: List[HomeResponse]
    total_pages: int
    page: int

class MovieResponse(BaseModel):
    id: int
    title: str | None = None
    overview: str | None = None
    release_date: str | None = None
    spoken_languages_names: str | None = None
    imdb_id: str | None = None