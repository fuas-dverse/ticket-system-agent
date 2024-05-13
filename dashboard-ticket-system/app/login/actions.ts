import { createClient } from "@/utils/supabase/server";
import {redirect} from "next/navigation";
import {Provider} from "@supabase/auth-js";

export const signInWithGoogle = async () => {
    "use server";

    const supabase = createClient();
    const {data, error} = await supabase.auth.signInWithOAuth({
        provider: 'google',
        options: {
            redirectTo: `${process.env.ROOT_URL}/auth/callback`,
        }
    })

    if (data.url) {
        redirect(data.url) // use the redirect API for your server framework
    }

    if (error) {
        return redirect("/login?message=Could not authenticate user");
    }

};

export const signInWithGithub = async () => {
    "use server";

    const supabase = createClient();
    const {data, error} = await supabase.auth.signInWithOAuth({
        provider: 'github',
        options: {
            redirectTo: `${process.env.ROOT_URL}/auth/callback`,
        }
    })

    if (data.url) {
        redirect(data.url) // use the redirect API for your server framework
    }

    if (error) {
        return redirect("/login?message=Could not authenticate user");
    }

};