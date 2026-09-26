import { apiFetch } from "./api";
import type { MoviePreview } from "./movies";
import type { User } from "./auth";

export type PostCreate = {
  movie_id: number;
  body: string;
  watch_if_you_enjoyed?: string | null;
  favourite_character?: string | null;
  favourite_part?: string | null;
};

export type Post = {
  id: number;
  body: string;
  watch_if_you_enjoyed?: string | null;
  favourite_character?: string | null;
  favourite_part?: string | null;
  created_at: string;
  author: User;
  movie: MoviePreview;
};

export function createPost(data: PostCreate, token: string) {
  return apiFetch<Post>("/posts", { method: "POST", body: JSON.stringify(data) }, token);
}