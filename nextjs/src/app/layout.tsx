import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "German → Ukrainian",
  description: "German to Ukrainian translation demo",
};

export default function RootLayout({ children }: LayoutProps<"/">) {
  return (
    <html lang="en" className="h-full antialiased">
      <body className="min-h-full flex flex-col font-sans">{children}</body>
    </html>
  );
}
