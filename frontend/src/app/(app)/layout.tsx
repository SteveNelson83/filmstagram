import { TopNav } from "@/components/layout/topNav";
import { FeedLayout } from "@/components/layout/feedLayout";
import ProtectedLayout from "@/components/layout/protectedLayout";
import { RightSidebar } from "@/components/sidebar/rightSidebar";

export default function AppLayout({ children }: { children: React.ReactNode }) {
    return (
        <>
            <ProtectedLayout>
                <div className="flex h-screen flex-col overflow-hidden">
                    <div className="text-center text-4xl bg-indigo-900 py-4">Filmstagram</div>
                    <TopNav />
                    <div className="min-h-0 flex-1 overflow-hidden">
                        <FeedLayout
                            left={<div>Under Construction</div>}
                            center={children}
                            right={<RightSidebar />}
                        />
                    </div>
                </div>
            </ProtectedLayout>
        </>
    );
}