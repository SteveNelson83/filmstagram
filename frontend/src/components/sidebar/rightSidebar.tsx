"use client";

import { UserCard, followUser, unfollowUser, getUserSuggestions } from "@/lib/users";
import { useAuth } from "@/context/authContext";
import { useEffect, useRef, useState } from "react";
import { UserSearch, type UserSearchHandle } from "../users/userSearch";
import { UserRow } from "../users/row";

export function RightSidebar() {
    const { token } = useAuth();
    const [suggestions, setSuggestions] = useState<UserCard[]>([]);
    const [togglingUserId, setTogglingUserId] = useState<number | null>(null);
    const [followError, setFollowError] = useState("");
    const userSearchRef = useRef<UserSearchHandle>(null);

    useEffect(() => {
        if (!token) return;
        getUserSuggestions(token, 3).then(setSuggestions).catch(() => setSuggestions([]));
    }, [token]);

    function applyFollowState(userId: number, isFollowing: boolean) {
        setSuggestions((prev) =>
            prev.map((u) => (u.id === userId ? { ...u, is_following: isFollowing } : u))
        );
    }

    async function handleFollowToggle(userId: number, isFollowing: boolean) {
        if (!token) return;

        setFollowError("");
        setTogglingUserId(userId);

        try {
            if (isFollowing) {
                await unfollowUser(userId, token);
            } else {
                await followUser(userId, token);
            }
            const nextFollowing = !isFollowing;
            applyFollowState(userId, nextFollowing);
            userSearchRef.current?.patchFollow(userId, nextFollowing);
        } catch (err) {
            setFollowError(
                err instanceof Error ? err.message : "Could not update follow"
            );
            throw err;
        } finally {
            setTogglingUserId(null);
        }
    }

    return (
        <div className="space-y-6 px-4 py-20 flex flex-col justify-around h-3/4">
            {followError && (
                <p className="text-sm text-red-400">{followError}</p>
            )}
            <section>
                <h2 className="mb-2 text-sm font-semibold text-slate-200">New Friends?</h2>
                {suggestions.map((u) => (
                    <UserRow
                        key={u.id}
                        user={u}
                        onFollowToggle={handleFollowToggle}
                        followBusy={togglingUserId === u.id}
                    />
                ))}
            </section>
            <UserSearch
                ref={userSearchRef}
                token={token}
                onFollowToggle={handleFollowToggle}
                togglingUserId={togglingUserId}
            />
        </div>
    );
}
