import { CreatePost } from "@/components/posts/createPost";

export default function CreatePostPage() {
    return (
        <div className="bg-slate-300 flex flex-col items-center justify-center h-full">
            <h1 className="text-4xl font-bold py-6 text-slate-500">Create a post</h1>
            <CreatePost />
        </div>
    );
}