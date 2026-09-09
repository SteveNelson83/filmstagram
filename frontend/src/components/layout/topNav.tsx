"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

const tabs = [
  { href: "/feed", label: "Feed" },
  { href: "/discover", label: "Discover" },
  { href: "/profile", label: "Profile" },
];

export function TopNav() {
  const pathname = usePathname();

  return (
    <nav className="flex h-16 items-center justify-center gap-8 border-b">
      {tabs.map((tab) => (
        <Link
          key={tab.href}
          href={tab.href}
          className={pathname === tab.href ? "font-semibold underline" : ""}
        >
          {tab.label}
        </Link>
      ))}
    </nav>
  );
}