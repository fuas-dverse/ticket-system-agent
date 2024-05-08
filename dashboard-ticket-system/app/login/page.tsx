"use client"
import {Button} from "@/components/ui/button";
import {signIn, useSession} from "next-auth/react";
import {useRouter} from "next/navigation";
import {useEffect} from "react";
import Image from "next/image";
import {Github} from 'lucide-react';

export default function Page() {
    const router = useRouter()
    const {data: session, status} = useSession();

    useEffect(() => {
        if (status === "authenticated") {
            router.push("/dashboard");
        }
    }, [router, session, status]);

    return (
        <div className="w-full h-screen lg:grid lg:min-h-[600px] lg:grid-cols-2 xl:min-h-[800px]">
            <div className="flex items-center justify-center py-12">
                <div className="mx-auto grid w-[350px] gap-6">
                    <div className="grid gap-2 text-center">
                        <h1 className="text-3xl font-bold">Login</h1>
                        <p className="text-balance text-muted-foreground">
                            Welcome the the DVerse Ticket System Dashboard App. In order to use our services you need to
                            login.
                        </p>
                    </div>
                    <div className="grid gap-4">
                        <Button onClick={() => signIn('github', {
                            callbackUrl: "/dashboard",
                            redirect: true
                        })} variant="outline" className="w-full">
                            Login with Github <Github className={"h-6 w-6 pl-2"}/>
                        </Button>
                        <Button onClick={() => signIn('google', {
                            callbackUrl: "/dashboard",
                            redirect: true
                        })} variant="outline" className="w-full">
                            Login with Google
                        </Button>
                    </div>
                </div>
            </div>
            <div className="hidden bg-muted lg:block">
                <Image
                    src="/defcon.jpg"
                    alt="Image"
                    width="1920"
                    height="1080"
                    className="h-full w-full object-cover dark:brightness-[0.2] dark:grayscale"
                />
            </div>
        </div>
    )
}