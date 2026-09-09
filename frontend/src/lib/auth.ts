import { apiFetch } from "./api";

export type User = {
  id: number;
  username: string;
  email: string;
  bio: string | null;
  avatar_url: string | null;
};

export async function login(email: string, password: string) {
  return apiFetch<{ access_token: string; token_type: string }>(
    "/auth/login",
    {
      method: "POST",
      body: JSON.stringify({ email, password }),
    }
  );
}

export async function register(username: string, email: string, password: string) {
    return apiFetch<User>("/auth/register", {
      method: "POST",
      body: JSON.stringify({ username, email, password }),
    });
  }

export async function getMe(token: string) {
  return apiFetch<User>("/users/me", {}, token);
}