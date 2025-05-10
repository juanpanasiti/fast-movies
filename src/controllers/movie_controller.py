import logging

from src.schemas.movies_schemas import NewMovieRequest, UpdateMovieRequest, MovieResponse
from src.exceptions.app_exceptions import NotFoundError
from src.exceptions.client_exceptions import NotFound
from src.exceptions.server_exceptions import InternalServerError

from src.services.movie_service import MovieService


logger = logging.getLogger(__name__)

class MovieController:
    def __init__(self, movie_service: MovieService = MovieService()):
        self.movie_service = movie_service

    async def get_movies(self) -> list[MovieResponse]:
        try:
            movies = await self.movie_service.get_movies()
            logger.debug(f'Encontradas {len(movies)} películas')
            return movies
        except Exception as e:
            logger.critical('Error no contemplado en get_movies()')
            raise InternalServerError(f"An error occurred while fetching movies: {str(e)}")

    async def get_movie(self, movie_id: int) -> MovieResponse:
        try:
            return await self.movie_service.get_movie(movie_id)
        except NotFoundError:
            logger.error(f'Movie #{movie_id} No encontrada en get_movie()')
            raise NotFound(f"Movie with id {movie_id} not found")
        except Exception as e:
            logger.critical('Error no contemplado en get_movie()')
            raise InternalServerError(f"An error occurred while fetching the movie: {str(e)}")

    async def create_movie(self, movie: NewMovieRequest) -> MovieResponse:
        try:
            return await self.movie_service.create_movie(movie)
        except Exception as e:
            logger.critical('Error no contemplado en create_movie()')
            raise InternalServerError(f"An error occurred while creating the movie: {str(e)}")

    async def update_movie(self, movie_id: int, movie: UpdateMovieRequest) -> MovieResponse:
        try:
            return await self.movie_service.update_movie(movie_id, movie)
        except NotFoundError:
            logger.error(f'Movie #{movie_id} No encontrada en update_movie()')
            raise NotFound(f"Movie with id {movie_id} not found")
        except Exception as e:
            logger.critical('Error no contemplado en update_movie()')
            raise InternalServerError(f"An error occurred while updating the movie: {str(e)}")

    async def delete_movie(self, movie_id: int) -> None:
        try:
            await self.movie_service.delete_movie(movie_id)
        except NotFoundError:

            logger.error(f'Movie #{movie_id} No encontrada en delete_movie()')
            raise NotFound(f"Movie with id {movie_id} not found")
        except Exception as e:
            logger.critical('Error no contemplado en delete_movie()')
            raise InternalServerError(f"An error occurred while deleting the movie: {str(e)}")
