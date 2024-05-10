import {Button} from "@/components/ui/button";
import Image from "next/image";
import {Github} from 'lucide-react';
import {signInWithGithub, signInWithGoogle} from "@/app/login/actions";

export default function Page() {
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
                    <form className="grid gap-4">
                        {/*<Button onClick={() => signIn('github', {*/}
                        {/*    callbackUrl: "/dashboard",*/}
                        {/*    redirect: true*/}
                        {/*})} variant="outline" className="w-full">*/}
                        {/*    Login with Github <Github className={"h-6 w-6 pl-2"}/>*/}
                        {/*</Button>*/}
                        <Button formAction={signInWithGithub} variant="outline" className="w-full">
                            Login with Github <Github className={"h-6 w-6 pl-2"}/>
                        </Button>
                        {/*<Button onClick={() => signIn('google', {*/}
                        {/*    callbackUrl: "/dashboard",*/}
                        {/*    redirect: true*/}
                        {/*})} variant="outline" className="w-full">*/}
                        {/*    Login with Google*/}
                        {/*</Button>*/}

                        <Button formAction={signInWithGoogle} variant="outline" className="w-full">
                            Login with Google
                        </Button>

                    </form>
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