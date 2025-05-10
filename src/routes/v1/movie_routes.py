from typing import Annotated

from fastapi import APIRouter, Path

from src.schemas.movies_schemas import NewMovieRequest, UpdateMovieRequest, MovieResponse
from .dependencies import movie_controller


router = APIRouter(
    prefix='/movies',
    responses={
        400: {'description': 'Bad Request. Revisa la info del body y/o parámetros'},
        500: {'description': 'Internal Server Error. Error del servidor no manejado, contacta al sysadmin'},
    }
)


@router.get(
    '',
    summary='Get all movies',
    description='Returns a list of all movies in the database',
)
async def get_movies() -> list[MovieResponse]:
    return await movie_controller.get_movies()


@router.get(
    '/{movie_id}',
    summary='Get a movie by ID',
    description='Returns a movie by its ID',
)
async def get_movie(
    movie_id: Annotated[int, Path(title='The ID of the movie to retrieve')]
) -> MovieResponse:
    return await movie_controller.get_movie(movie_id)


@router.post(
    '',
    status_code=201,
    summary='Create a new movie',
    description='Creates a new movie in the database',
)
async def create_movie(movie: NewMovieRequest) -> MovieResponse:
    return await movie_controller.create_movie(movie)


@router.put(
    '/{movie_id}',
    summary='Update a movie by ID',
    description='Updates a movie by its ID',
)
async def update_movie(
    movie_id: Annotated[int, Path(title='The ID of the movie to update')],
    movie: UpdateMovieRequest
) -> MovieResponse:
    return await movie_controller.update_movie(movie_id, movie)


@router.delete(
    '/{movie_id}',
    status_code=204,
    summary='Delete a movie by ID',
    description='Deletes a movie by its ID',
)
async def delete_movie(
    movie_id: Annotated[int, Path(title='The ID of the movie to delete')]
) -> None:
    return await movie_controller.delete_movie(movie_id)
