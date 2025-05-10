from typing import Optional, List
from datetime import date, datetime

from pydantic import BaseModel, Field
from pydantic_tooltypes import Partial


class NewMovieRequest(BaseModel):
    title: str = Field(..., example="Inception")
    year: int = Field(..., example=2010)
    director: str = Field(..., example="Christopher Nolan")
    viewed: bool = Field(..., example=True)


class UpdateMovieRequest(Partial[NewMovieRequest]):
    pass


class MovieResponse(NewMovieRequest):
    id: int = Field(..., example=1)
    created_at: datetime = Field(..., example="2023-10-01T12:00:00Z")
    updated_at: datetime = Field(..., example="2023-10-01T12:00:00Z")
