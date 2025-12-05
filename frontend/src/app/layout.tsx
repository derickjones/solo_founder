import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import { ClerkProvider } from '@clerk/nextjs'
import "./globals.css";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "Gospel Study Assistant",
  description: "AI-powered gospel study tools for The Church of Jesus Christ of Latter-day Saints",
};

// Check if Clerk is configured
const clerkPublishableKey = process.env.NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY;
const isClerkConfigured = clerkPublishableKey && clerkPublishableKey !== 'your_clerk_publishable_key_here';

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  const content = (
    <html lang="en">
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased`}
      >
        {children}
      </body>
    </html>
  );

  // Only use ClerkProvider if Clerk is properly configured
  if (isClerkConfigured) {
    return (
      <ClerkProvider>
        {content}
      </ClerkProvider>
    );
  }

  // Return content without Clerk for development/demo mode
  return content;
}
