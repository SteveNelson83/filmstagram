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
        <div className="grid min-h-[calc(100vh-4rem)] grid-cols-12">
            <aside className="col-span-3 bg-indigo-900">{left}</aside>
            <main className="col-span-6">{center}</main>
            <aside className="col-span-3 bg-indigo-900">{right}</aside>
        </div>
    );
}