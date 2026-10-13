import { FeedPosts } from "@/components/posts/feedPosts";

export default function FeedPage() {
    return (
        <div className="mx-auto max-w-2xl px-4">
            <h1 className="pt-4 text-xl font-semibold text-slate-400 text-center">Latest Posts</h1>
            <FeedPosts />
        </div>
    );
}