export function Avatar({ url, username }: { url: string | null; username: string }) {
    if (url) {
        return <img src={url} alt="" className="h-10 w-10 rounded-full object-cover" />;
    }
    return (
        <div
            className="flex h-10 w-10 shrink-0 items-center justify-center rounded-full bg-slate-300 text-sm font-medium text-slate-600"
            aria-hidden
        >
            {username.charAt(0).toUpperCase()}
        </div>
    );
}