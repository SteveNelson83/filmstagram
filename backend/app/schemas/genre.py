from pydantic import BaseModel


class GenreResponse(BaseModel):
    id: int
    tmdb_id: int
    name: str

    model_config = {
        "from_attributes": True
    }