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
      <div className="grid min-h-[calc(100vh-4rem)] grid-cols-12 gap-4 px-4">
        <aside className="col-span-3">{left}</aside>
        <main className="col-span-6">{center}</main>
        <aside className="col-span-3">{right}</aside>
      </div>
    );
  }