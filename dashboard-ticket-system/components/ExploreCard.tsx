"use client"
import {Card, CardContent} from "@/components/ui/card";
import {Button} from "@/components/ui/button";
import {IAvailableAPI} from "@/app/dashboard/explore/page";
import {useRouter} from "next/navigation";

interface Props {
    api: IAvailableAPI
}

export default function ExploreCard ({api}: Props){
    const router = useRouter()
    return (
        <Card>
            <CardContent className="flex flex-col gap-4">
                <div className="space-y-2">
                    <h3 className="text-lg font-semibold">{api.name}</h3>
                    <p className="text-sm text-gray-500 dark:text-gray-400">
                        {api.description.substring(0, 100)}
                        {api.description.length > 100 ? "..." : ""}
                    </p>
                </div>
                <Button size="sm" onClick={() => {
                    router.push("/dashboard/explore/" + api.id)
                }}>View Details</Button>
            </CardContent>
        </Card>
    )
}