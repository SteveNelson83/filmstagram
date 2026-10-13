"use client";

import { useCallback, useEffect, useState } from "react";
import { useAuth } from "@/context/authContext";
import { getFeed, type Post } from "@/lib/posts";
import { PostCard } from "./postCard";

export function FeedPosts() {
    const { token } = useAuth();
    const [posts, setPosts] = useState<Post[]>([]);
    const [hasMore, setHasMore] = useState(false);
    const [nextOffset, setNextOffset] = useState(0);
    const [loading, setLoading] = useState(true);
    const [loadingMore, setLoadingMore] = useState(false);
    const [error, setError] = useState("");

    const loadPage = useCallback(
        async (offset: number, append: boolean) => {
            if (!token) return;

            if (append) {
                setLoadingMore(true);
            } else {
                setLoading(true);
            }
            setError("");

            try {
                const feed = await getFeed(token, 30, offset);
                setPosts((prev) => (append ? [...prev, ...feed.items] : feed.items));
                setHasMore(feed.has_more);
                setNextOffset(
                    feed.next_offset ?? offset + feed.items.length
                );
            } catch (err) {
                setError(
                    err instanceof Error ? err.message : "Could not load feed"
                );
                if (!append) setPosts([]);
            } finally {
                setLoading(false);
                setLoadingMore(false);
            }
        },
        [token]
    );

    useEffect(() => {
        if (!token) {
            setPosts([]);
            setLoading(false);
            return;
        }
        loadPage(0, false);
    }, [token, loadPage]);

    if (loading) {
        return (
            <div className="space-y-4 py-4">
                {[1, 2].map((i) => (
                    <div
                        key={i}
                        className="h-48 animate-pulse rounded-2xl bg-slate-200"
                        aria-hidden
                    />
                ))}
            </div>
        );
    }

    return (
        <div className="space-y-6 py-4">
            {error && <p className="text-sm text-red-600">{error}</p>}

            {posts.length === 0 && !error && (
                <p className="rounded-xl border border-dashed border-slate-300 bg-white/50 p-6 text-center text-slate-600">
                    Follow other film dorks and check back here for
                    their posts.
                </p>
            )}

            {posts.map((post) => (
                <PostCard key={post.id} {...post} />
            ))}

            {hasMore && (
                <div className="flex justify-center pb-6 pt-2">
                    <button
                        type="button"
                        disabled={loadingMore}
                        onClick={() => loadPage(nextOffset, true)}
                        className="rounded-md border border-slate-600 bg-slate-700 px-6 py-2 text-sm font-medium text-white disabled:cursor-not-allowed disabled:opacity-50"
                    >
                        {loadingMore ? "Loading…" : "Load more posts"}
                    </button>
                </div>
            )}
        </div>
    );
}
