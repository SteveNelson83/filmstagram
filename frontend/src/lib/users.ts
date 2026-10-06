import { apiFetch } from "./api";

export type UserCard = {
    id: number;
    username: string;
    avatar_url: string | null;
    is_following: boolean;
};

export function getUserSuggestions(token: string, limit = 3) {
    return apiFetch<UserCard[]>(`/users/suggestions?limit=${limit}`, {}, token);
}

export function searchUsers(query: string, token: string, limit = 20) {
    const params = new URLSearchParams({ query, limit: String(limit) });
    return apiFetch<UserCard[]>(`/users/search?${params}`, {}, token);
}

export function followUser(userId: number, token: string) {
    return apiFetch<void>(`/users/${userId}/follow`, { method: "POST" }, token)
}

export function unfollowUser(userId: number, token: string) {
    return apiFetch<void>(`/users/${userId}/follow`, { method: "DELETE" }, token)
}