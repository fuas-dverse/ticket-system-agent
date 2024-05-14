import type {Metadata} from "next";
import {Inter as FontSans} from "next/font/google"
import "./globals.css";
import {cn} from "@/lib/utils"

const defaultUrl = process.env.VERCEL_URL
    ? `https://${process.env.VERCEL_URL}`
    : "http://localhost:3000";

const fontSans = FontSans({
    subsets: ["latin"],
    variable: "--font-sans",
})

export const metadata: Metadata = {
    metadataBase: new URL(defaultUrl),
    title: "Ticket System Dashboard",
    description: "The Dashboard for managing API keys and usage",
};

export default function RootLayout(
    {
        children,
    }: Readonly<{
        children: React.ReactNode;
    }>) {
    return (
        <html lang="en">
        <body
            className={cn(
                "min-h-screen font-sans antialiased",
                fontSans.variable
            )}
        >
        {/*<Providers>*/}
            {children}
        {/*</Providers>*/}
        </body>
        </html>
    );
}
