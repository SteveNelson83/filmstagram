export function FeedLayout({
    left,
    center,
    right,
}: {
    left: React.ReactNode;
    center: React.ReactNode;
    right: React.ReactNode;
}) {
    return (
        <div className="grid h-full min-h-0 overflow-hidden grid-cols-12">
            <aside className="col-span-3 h-full bg-indigo-900">{left}</aside>
            <main className="col-span-6 h-full min-h-0 overflow-y-auto feed-scroll">{center}</main>
            <aside className="col-span-3 h-full bg-indigo-900">{right}</aside>
        </div>
    );
}