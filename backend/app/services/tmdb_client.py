import httpx

from app.schemas.tmdb import TmdbDiscoverResponse, TmdbGenreListResponse, TmdbMovie
from app.db.database import settings

class TmdbClient:
    def __init__(self):
        self.base_url = settings.TMDB_BASE_URL.rstrip("/")
        self.api_key = settings.TMDB_API_KEY

    def _get(self, path: str, params: dict | None = None) -> dict:
        params = params or {}
        params["api_key"] = self.api_key

        url = f"{self.base_url}/{path.lstrip('/')}"

        response = httpx.get(url, params=params, timeout=10.0)
        response.raise_for_status()
        return response.json()

    def get_genre_list(self) -> TmdbGenreListResponse:
        data = self._get("genre/movie/list")
        return TmdbGenreListResponse.model_validate(data)

    def get_movie(self, tmdb_id: int) -> TmdbMovie:
        data = self._get(f"movie/{tmdb_id}")
        return TmdbMovie.model_validate(data)

    def discover_movies(self, page: int = 1, **filters) -> TmdbDiscoverResponse:
        params = {"page": page, **filters}
        data = self._get("discover/movie", params=params)
        return TmdbDiscoverResponse.model_validate(data)