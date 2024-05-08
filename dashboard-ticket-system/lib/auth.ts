import NextAuth, {NextAuthOptions} from "next-auth";
import Github from "next-auth/providers/github";

export const authOptions: NextAuthOptions = {
    providers: [
        Github({
            clientId: process.env.GITHUB_CLIENT_ID as string,
            clientSecret: process.env.GITHUB_CLIENT_SECRET as string,
        })
    ],
    secret: process.env.NEXT_AUTH_SECRET,
    callbacks: {}
}

export const { handlers, signIn, signOut, auth } = NextAuth(authOptions)