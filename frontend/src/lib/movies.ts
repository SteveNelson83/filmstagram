import { apiFetch } from "./api";

export type MovieSearchResult = {
    id: number;
    title: string;
    release_year: number | null;
    poster_path: string | null;
    poster_url: string | null;
}

export type CastPreview = { 
    name: string;
    character: string;
}

export type MoviePreview = {
    id: number;
    title: string;
    release_year: number | null;
    poster_path: string | null;
    poster_url: string | null;
    directors: string[];
    top_cast: CastPreview[];
}

export function searchMovies(query: string, limit = 10) {
    const params = new URLSearchParams({ query, limit: String(limit) });
    return apiFetch<MovieSearchResult[]>(`/movies/search?${params}`);
}

export function getMoviePreview(movieId: number) {
    return apiFetch<MoviePreview>(`/movies/${movieId}/preview`);
}