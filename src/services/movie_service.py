from datetime import datetime

from src.helpers.file_helpers import read_json_file, write_json_file
from src.schemas.movies_schemas import NewMovieRequest, UpdateMovieRequest, MovieResponse
from src.exceptions.app_exceptions import NotFoundError

MOVIES_JSON_FILE = 'fake_db.json'


class MovieService:
    async def get_movies(self) -> list[MovieResponse]:
        movies_list = await self.__get_movies_list()
        return [MovieResponse(**movie) for movie in movies_list]

    async def get_movie(self, movie_id: int) -> MovieResponse:
        movie = await self.__get_by_id(movie_id)
        if not movie:
            raise NotFoundError(f'Movie with id {movie_id} not found')
        return MovieResponse(**movie)

    async def create_movie(self, movie: NewMovieRequest) -> MovieResponse:
        movie_dict = movie.model_dump()
        saved_movie = await self.__save_movie(movie_dict)
        return MovieResponse(**saved_movie)

    async def update_movie(self, movie_id: int, movie: UpdateMovieRequest) -> MovieResponse:
        old_data = await self.__get_by_id(movie_id)
        if not old_data:
            raise NotFoundError(f'Movie with id {movie_id} not found')
        movie_dict = movie.model_dump(exclude_none=True)
        old_data.update(movie_dict)
        updated_movie = await self.__save_movie(old_data)
        return MovieResponse(**updated_movie)
    
    async def delete_movie(self, movie_id: int) -> None:
        movies_list = await self.__get_movies_list()
        for movie in movies_list:
            if movie['id'] == movie_id:
                movies_list.remove(movie)
                write_json_file(MOVIES_JSON_FILE, movies_list)
                return
        raise NotFoundError(f'Movie with id {movie_id} not found')

    # Private methods

    async def __get_movies_list(self) -> list[dict]:
        movies_list = read_json_file(MOVIES_JSON_FILE)
        return movies_list

    async def __save_movie(self, movie_dict: dict) -> dict:
        movies_list = await self.__get_movies_list()
        is_new = False
        if not movie_dict.get('id'):
            movie_dict['id'] = await self.__get_next_id()
            movie_dict['created_at'] = datetime.now().isoformat()
            is_new = True
        movie_dict['updated_at'] = datetime.now().isoformat()

        if not is_new:
            for i, movie in enumerate(movies_list):
                if movie['id'] == movie_dict['id']:
                    movies_list[i] = movie_dict
                    break
        else:
            movies_list.append(movie_dict)
        write_json_file(MOVIES_JSON_FILE, movies_list)
        return movie_dict

    async def __get_next_id(self) -> int:
        movies_list = await self.__get_movies_list()
        if not movies_list:
            return 1
        return max(movie['id'] for movie in movies_list) + 1

    async def __get_by_id(self, movie_id: int) -> dict | None:
        movies_list = await self.__get_movies_list()
        for movie in movies_list:
            if movie['id'] == movie_id:
                return movie
        return None
