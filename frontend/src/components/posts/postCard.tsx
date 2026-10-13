"use client";

import { Avatar } from "../users/avatar";
import { Post } from "@/lib/posts";

const posterClass = "h-96 w-64 shrink-0 rounded bg-slate-300";
const textClass = "mt-1 text-sm text-slate-700";

function formatPostDate(iso: string): string {
    const d = new Date(iso);
    const day = String(d.getDate()).padStart(2, "0");
    const month = String(d.getMonth() + 1).padStart(2, "0");
    const year = String(d.getFullYear()).slice(-2);
    return `${day}-${month}-${year}`;
}

export function PostCard(post: Post) {
    return (
        <div className="bg-slate-200 rounded-md p-2">
            <div className="flex gap-2 text-slate-600 pb-2 items-center">
                <Avatar url="" username={post.author.username} />
                <h2>{post.author.username}</h2>
                <h2>{formatPostDate(post.created_at)}</h2>
            </div>
            <div className="flex items-start gap-4">
                {post.movie.poster_url ? (
                    <img
                        src={post.movie.poster_url}
                        alt={post.movie.title}
                        className={`${posterClass} object-cover bg-transparent`}
                    />
                ) : (
                    <div className={posterClass} aria-hidden />
                )}

                <div className="min-w-0 flex-1">
                    <h2 className="font-semibold text-slate-900">
                        {post.movie.title}
                        {post.movie.release_year != null &&
                            ` (${post.movie.release_year})`}
                        {post.movie.directors.length > 0 && (
                            <p className={textClass}>
                                Dir: {post.movie.directors.join(", ")}
                            </p>
                        )}
                        {post.movie.top_cast.length > 0 && (
                            <p className={textClass}>
                                Cast: {post.movie.top_cast.map((m) => m.name).join(", ")}
                            </p>
                        )}
                    </h2>
                    <p className="text-slate-700">...</p>
                    {post.body.length > 0 && (
                        <p className={textClass}>
                            {post.body}
                        </p>
                    )}
                    ...
                    {post.watch_if_you_enjoyed && (
                        <p className={textClass}>
                            Watch if you enjoyed: {post.watch_if_you_enjoyed}
                        </p>
                    )}
                    ...
                    {post.favourite_character && (
                        <p className={textClass}>
                            Favourite Character: {post.favourite_character}
                        </p>
                    )}
                    ...
                    {post.favourite_part && (
                        <p className={textClass}>
                            Favourite bit: {post.favourite_part}
                        </p>
                    )}
                </div>
            </div>
        </div>
    );
}
