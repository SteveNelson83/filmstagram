TMDB_POSTER_BASE = "https://image.tmdb.org/t/p/w500"

def poster_url_from_path(poster_path: str | None) -> str | None:
    if not poster_path:
        return None
    return f"{TMDB_POSTER_BASE}{poster_path}"