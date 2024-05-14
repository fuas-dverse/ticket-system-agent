"use client"

import {Input} from "@/components/ui/input";
import {useEffect, useState} from "react";
import {createClient} from "@/utils/supabase/client";
import ExploreCard from "@/components/ExploreCard";

export interface IAvailableAPI {
    id: string
    name: string
    description: string
    endpoint: string
    website: string
    active: boolean
}

export default function Page() {
    const [apis, setApis] = useState<IAvailableAPI[]>([])
    const supabase = createClient()

    async function fetchApis() {
        const {data, error} = await supabase.from("available_apis").select("*")

        if (error) {
            console.error(error)
        } else {
            setApis(data)
        }
    }


    useEffect(() => {
        fetchApis()

        console.log("APIs", apis)
    }, [supabase])

    return (
        <div className="py-4">
            <h1 className={"text-2xl font-bold"}>Explore</h1>
            <div className="flex flex-col gap-6 md:gap-8 my-4">
                <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
                    <form className="flex-1 max-w-md">
                        <Input className="bg-white dark:bg-gray-800" placeholder="Search keys..."/>
                    </form>
                </div>
                <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6 md:gap-8">
                    {
                        apis.map((api) => {
                            return <ExploreCard api={api} key={api.id}/>
                        })
                    }
                </div>
            </div>
        </div>
    )
}