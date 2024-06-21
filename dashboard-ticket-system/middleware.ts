import {type NextRequest, NextResponse} from 'next/server';
import {updateSession} from "@/utils/supabase/middleware";

export async function middleware(request: NextRequest) {
    try {
        if (request.nextUrl.pathname === '/') {
            const url = request.nextUrl.clone()
            url.pathname = '/login';
            return NextResponse.rewrite(url)
        }

        return await updateSession(request);
    } catch (error) {
        console.error('Middleware error:', error);
        return new Response('Internal Server Error', {status: 500});
    }
}

export const config = {
    matcher: [
        "/((?!_next/static|_next/image|favicon.ico|.*\\.(?:svg|png|jpg|jpeg|gif|webp)$).*)",
    ],
};