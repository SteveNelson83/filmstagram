import { TopNav } from "@/components/layout/topNav";
import { FeedLayout } from "@/components/layout/feedLayout";
import ProtectedLayout from "@/components/layout/protectedLayout";
import { RightSidebar } from "@/components/sidebar/rightSidebar";

export default function AppLayout({ children }: { children: React.ReactNode }) {
    return (
        <>
            <ProtectedLayout>
                <TopNav />
                <FeedLayout
                    left={<div>Left sidebar (suggestions, etc.)</div>}
                    center={children}
                    right={<RightSidebar />}
                />
            </ProtectedLayout>
        </>
    );
}