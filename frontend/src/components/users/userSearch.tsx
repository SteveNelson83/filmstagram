"use client";

import { forwardRef, useEffect, useImperativeHandle, useState } from "react";
import { UserRow } from "./row";
import { UserCard, searchUsers } from "@/lib/users";

export type UserSearchHandle = {
    patchFollow: (userId: number, isFollowing: boolean) => void;
};

type Props = {
    token: string | null;
    onFollowToggle: (userId: number, currentlyFollowing: boolean) => Promise<void>;
    togglingUserId: number | null;
};

export const UserSearch = forwardRef<UserSearchHandle, Props>(function UserSearch(
    { token, onFollowToggle, togglingUserId },
    ref
) {
    const [searchQuery, setSearchQuery] = useState("");
    const [searchResults, setSearchResults] = useState<UserCard[]>([]);
    const [isDropdownOpen, setIsDropdownOpen] = useState(false);
    const [searching, setSearching] = useState(false);

    useImperativeHandle(ref, () => ({
        patchFollow(userId: number, isFollowing: boolean) {
            setSearchResults((prev) =>
                prev.map((u) =>
                    u.id === userId ? { ...u, is_following: isFollowing } : u
                )
            );
        },
    }));

    useEffect(() => {
        if (!isDropdownOpen || !token) {
            return;
        }

        const q = searchQuery.trim();
        if (q.length < 2) {
            setSearchResults([]);
            setSearching(false);
            return;
        }

        setSearching(true);
        let cancelled = false;
        const timer = setTimeout(() => {
            searchUsers(q, token)
                .then((results) => {
                    if (!cancelled) setSearchResults(results);
                })
                .catch(() => {
                    if (!cancelled) setSearchResults([]);
                })
                .finally(() => {
                    if (!cancelled) setSearching(false);
                });
        }, 300);

        return () => {
            cancelled = true;
            clearTimeout(timer);
        };
    }, [searchQuery, isDropdownOpen, token]);

    async function handleFollow(userId: number, isFollowing: boolean) {
        try {
            await onFollowToggle(userId, isFollowing);
        } catch {
            // Parent shows followError
        }
    }

    return (
        <div className="relative">
            <h2 className="mb-2 text-sm font-semibold text-slate-200">Search by username</h2>
            <input
                type="search"
                value={searchQuery}
                onChange={(e) => {
                    setSearchQuery(e.target.value);
                    setIsDropdownOpen(true);
                }}
                placeholder="Start typing..."
                className="w-full rounded-md border bg-slate-300 border-slate-800 p-2 text-slate-800 placeholder:text-slate-400"
            />
            {searching && isDropdownOpen && searchQuery.trim().length >= 2 && (
                <p className="absolute left-0 right-0 top-full z-50 mt-1 rounded-md border border-slate-200 bg-white px-3 py-2 text-sm text-slate-500 shadow-lg">
                    Searching…
                </p>
            )}
            {isDropdownOpen && !searching && searchResults.length > 0 && (
                <ul className="absolute left-0 right-0 top-full z-50 mt-1 max-h-48 overflow-y-auto rounded-md border border-slate-200 bg-white shadow-lg">
                    {searchResults.map((user) => (
                        <li key={user.id}>
                            <UserRow
                                user={user}
                                onFollowToggle={handleFollow}
                                followBusy={togglingUserId === user.id}
                            />
                        </li>
                    ))}
                </ul>
            )}
        </div>
    );
});
