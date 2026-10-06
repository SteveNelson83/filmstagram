"use client";

import { Avatar } from "./avatar";
import { UserCard } from "@/lib/users";

type Props = {
    user: UserCard;
    onFollowToggle: (userId: number, currentlyFollowing: boolean) => void | Promise<void>;
    followBusy?: boolean;
};

export function UserRow({ user, onFollowToggle, followBusy }: Props) {
    return (
        <div className="flex items-center gap-3 py-2 px-4">
            <Avatar url={user.avatar_url} username={user.username} />
            <span className="min-w-0 flex-1 truncate font-medium text-slate-400">
                {user.username}
            </span>
            <button
                type="button"
                disabled={followBusy}
                onClick={() => onFollowToggle(user.id, user.is_following)}
                className="shrink-0 cursor-pointer rounded-md border border-slate-600 bg-indigo-900 px-3 py-1 text-sm text-white disabled:cursor-not-allowed disabled:opacity-50"
            >
                {user.is_following ? "Following" : "Follow"}
            </button>
        </div>
    );
}
