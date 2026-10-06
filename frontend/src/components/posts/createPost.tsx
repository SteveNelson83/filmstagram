"use client";

import { useRouter } from "next/navigation";
import { useEffect, useState, type SubmitEvent } from "react";
import { useAuth } from "@/context/authContext";
import {
    getMoviePreview,
    searchMovies,
    type MoviePreview,
    type MovieSearchResult,
} from "@/lib/movies";
import { createPost } from "@/lib/posts";

export function CreatePost() {
    const { token } = useAuth();
    const router = useRouter();

    const [searchQuery, setSearchQuery] = useState("");
    const [searchResults, setSearchResults] = useState<MovieSearchResult[]>([]);
    const [selectedMovie, setSelectedMovie] = useState<MoviePreview | null>(null);
    const [isDropdownOpen, setIsDropdownOpen] = useState(false);
    const [previewLoading, setPreviewLoading] = useState(false);

    const [body, setBody] = useState("");
    const [watchIfYouEnjoyed, setWatchIfYouEnjoyed] = useState("");
    const [favouriteCharacter, setFavouriteCharacter] = useState("");
    const [favouritePart, setFavouritePart] = useState("");

    const [error, setError] = useState("");
    const [submitting, setSubmitting] = useState(false);

    // Debounced search (backend min 3 chars)
    useEffect(() => {
        if (!isDropdownOpen) {
            return;
        }

        const q = searchQuery.trim();
        if (q.length < 3) {
            setSearchResults([]);
            return;
        }

        let cancelled = false;
        const timer = setTimeout(() => {
            searchMovies(q, 8)
                .then((results) => {
                    if (!cancelled) setSearchResults(results);
                })
                .catch(() => {
                    if (!cancelled) setSearchResults([]);
                });
        }, 300);

        return () => {
            cancelled = true;
            clearTimeout(timer);
        };
    }, [searchQuery, isDropdownOpen]);

    async function selectMovie(result: MovieSearchResult) {
        setIsDropdownOpen(false);
        setSearchResults([]);
        setSearchQuery(result.title);
        setError("");
        setPreviewLoading(true);

        try {
            const preview = await getMoviePreview(result.id);
            setSelectedMovie(preview);
        } catch {
            setError("Could not load movie preview");
        } finally {
            setPreviewLoading(false);
        }
    }

    async function handleSubmit(e: SubmitEvent) {
        e.preventDefault();
        if (!token || !selectedMovie) return;

        setError("");
        setSubmitting(true);

        try {
            await createPost(
                {
                    movie_id: selectedMovie.id,
                    body: body.trim(),
                    watch_if_you_enjoyed: watchIfYouEnjoyed.trim() || null,
                    favourite_character: favouriteCharacter.trim() || null,
                    favourite_part: favouritePart.trim() || null,
                },
                token
            );
            router.push("/feed");
        } catch (err) {
            setError(err instanceof Error ? err.message : "Could not create post");
        } finally {
            setSubmitting(false);
        }
    }

    const inputClass = "w-full rounded-md border bg-slate-300 border-slate-800 p-2 text-slate-800 placeholder:text-slate-400";
    const posterClass = "h-54 w-36 shrink-0 rounded bg-slate-300";

    return (
        <form onSubmit={handleSubmit} className="space-y-4 bg-white w-[450px] h-auto p-4 rounded-2xl flex flex-col justify-center text-slate-500">
            {error && <p className="text-sm text-red-600">{error}</p>}
            {/* 1. Movie search */}
            <section className="space-y-2">
                <label className="block text-sm font-medium text-slate-700">
                    Movie
                </label>
                <div className="relative">
                    <input
                        type="search"
                        value={searchQuery}
                        onChange={(e) => {
                            setSearchQuery(e.target.value);
                            setIsDropdownOpen(true);
                        }}
                        placeholder="Start typing..."
                        className={inputClass}
                    />
                    {isDropdownOpen && searchResults.length > 0 && (
                        <ul className="absolute left-0 right-0 top-full z-50 mt-1 max-h-48 overflow-y-auto rounded-md border border-slate-200 bg-white shadow-lg">
                            {searchResults.map((movie) => (
                                <li key={movie.id}>
                                    <button
                                        type="button"
                                        onClick={() => selectMovie(movie)}
                                        className="flex w-full items-center gap-3 px-3 py-2 text-left hover:bg-slate-50 cursor-pointer"
                                    >
                                        {movie.poster_url && (
                                            <img
                                                src={movie.poster_url}
                                                alt=""
                                                className="h-12 w-8 rounded object-cover"
                                            />
                                        )}
                                        <span>
                                            {movie.title}
                                            {movie.release_year ? ` (${movie.release_year})` : ""}
                                        </span>
                                    </button>
                                </li>
                            ))}
                        </ul>
                    )}
                </div>
            </section>
            {/* 2. Movie preview */}
            <section className="rounded-xl border border-slate-200 bg-white p-4">
                {previewLoading ? (
                    /* Loading skeleton */
                    <div className="flex gap-4">
                        <div className={`${posterClass} animate-pulse`} aria-hidden />
                        <div className="min-w-0 flex-1 space-y-2">
                            <div className="h-5 w-4/5 animate-pulse rounded bg-slate-300" />
                            <div className="h-4 w-24 animate-pulse rounded bg-slate-300" />
                            <div className="h-4 w-full animate-pulse rounded bg-slate-300" />
                        </div>
                    </div>
                ) : selectedMovie ? (
                    <div className="flex gap-4">
                        {selectedMovie.poster_url ? (
                            <img
                                src={selectedMovie.poster_url}
                                alt={selectedMovie.title}
                                className={`${posterClass} object-cover bg-transparent`}
                            />
                        ) : (
                            <div className={posterClass} aria-hidden />
                        )}

                        <div className="min-w-0 flex-1">
                            <h2 className="font-semibold text-slate-900">
                                {selectedMovie.title}
                                {selectedMovie.release_year != null &&
                                    ` (${selectedMovie.release_year})`}
                            </h2>
                            ...
                            {selectedMovie.directors.length > 0 && (
                                <p className="mt-1 text-sm text-slate-700">
                                    Dir: {selectedMovie.directors.join(", ")}
                                </p>
                            )}
                            ...
                            {selectedMovie.top_cast.length > 0 && (
                                <p className="mt-1 text-sm text-slate-700">
                                    Cast: {selectedMovie.top_cast.map((m) => m.name).join(", ")}
                                </p>
                            )}
                        </div>
                    </div>
                ) : (
                    <div className="flex gap-4">
                        <div className={posterClass} aria-hidden />
                        <div className="min-w-0 flex-1">
                            <h2 className="font-semibold text-slate-400">Movie Title (year)</h2>
                            ...
                            <p className="mt-1 text-sm text-slate-400">Dir: -</p>
                            ...
                            <p className="mt-1 text-sm text-slate-400">Cast: -</p>
                        </div>
                    </div>
                )}
            </section>

            {/* 3. Required review */}
            <section className="space-y-2">
                <label className="block text-sm font-medium text-slate-700">
                    What's so great about it? <span className="text-red-500">*</span>
                </label>
                <textarea
                    value={body}
                    onChange={(e) => setBody(e.target.value)}
                    required
                    rows={4}
                    className={inputClass}
                />
            </section>

            {/* 4. Optional fields */}
            <section className="space-y-3 rounded-xl border border-dashed border-slate-200 p-4">
                <label className="block text-sm font-medium text-slate-700">
                    Favourite character:
                </label>
                <input
                    type="text"
                    value={favouriteCharacter}
                    onChange={(e) => setFavouriteCharacter(e.target.value)}
                    className={inputClass}
                />
                <label className="block text-sm font-medium text-slate-700">
                    Favourite part:
                </label>
                <input
                    type="text"
                    value={favouritePart}
                    onChange={(e) => setFavouritePart(e.target.value)}
                    className={inputClass}
                />
                <label className="block text-sm font-medium text-slate-700">
                    Watch if you enjoyed:
                </label>
                <input
                    type="text"
                    value={watchIfYouEnjoyed}
                    onChange={(e) => setWatchIfYouEnjoyed(e.target.value)}
                    className={inputClass}
                />
            </section>

            <button
                type="submit"
                disabled={!selectedMovie || previewLoading || !body.trim() || submitting}
                className="w-full rounded-md bg-slate-600 py-2 text-white disabled:cursor-not-allowed disabled:opacity-50"
            >
                {submitting ? "Posting…" : "Post your post"}
            </button>
        </form>
    );
}