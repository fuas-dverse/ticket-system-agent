import { type NextRequest, NextResponse } from 'next/server';
import { updateSession } from "@/utils/supabase/middleware";

export async function middleware(request: NextRequest) {
    // Check if the requested URL is the root
    if (request.nextUrl.pathname === '/') {
        // Create a redirect response to the /login page
        return NextResponse.redirect(process.env.ROOT_URL + '/login');
    }

    return await updateSession(request);
}

export const config = {
    matcher: [
        "/((?!_next/static|_next/image|favicon.ico|.*\\.(?:svg|png|jpg|jpeg|gif|webp)$).*)",
    ],
};