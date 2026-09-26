export default function AuthLayout({
    children,
}: {
    children: React.ReactNode;
}) {
    return (
        <div className="min-h-screen bg-slate-300 flex flex-col items-center justify-center">
            <h1 className="text-4xl font-bold pb-8">Filmstagram</h1>
            {children}
        </div>
    );
}