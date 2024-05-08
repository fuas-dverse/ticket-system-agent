"use client"
import {Button} from "@/components/ui/button";
import {signIn, useSession} from "next-auth/react";
import {useRouter} from "next/navigation";
import {useEffect} from "react";

export default function Page() {
    const router = useRouter()
    const {data: session, status} = useSession();

    useEffect(() => {
        if (status === "authenticated") {
            router.push("/dashboard");
        }
    }, [router, session, status]);

    return (
        <div>
            Login
            <Button onClick={() => signIn('github', {
                redirect: true,
                callbackUrl: "/dashboard",
            })}></Button>
        </div>
    )
}