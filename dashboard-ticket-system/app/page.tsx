"use client"

import {Button} from "@/components/ui/button";
import {signIn} from "@/lib/auth";

export default function Page() {
    return (
        <div>
            Login
            <Button onClick={() => signIn('github')}></Button>
        </div>
    )
}