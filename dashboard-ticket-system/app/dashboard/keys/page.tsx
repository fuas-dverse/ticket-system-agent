"use client";
import {Button} from "@/components/ui/button";
import {SearchIcon} from "lucide-react";
import {Input} from "@/components/ui/input";
import {Table, TableBody, TableCell, TableHead, TableHeader, TableRow} from "@/components/ui/table";
import KeysTableRow from "@/components/keys/TableRow";
import Link from "next/link";
import {usePathname, useSearchParams} from "next/navigation";
import {useEffect, useState} from "react";
import {useToast} from "@/components/ui/use-toast";
import {Toaster} from "@/components/ui/toaster";
import {createClient} from "@/utils/supabase/client";

export interface IKeys {
    id: string;
    name: string;
    key: string;
    api_url: string;
    created: string;
    lastUsed: string;
}

export default function Page() {
    // const {data: todos} = await supabaseClient.from('todos').select()
    const params = useSearchParams()
    const newKeyCreated = params.get("newKeyCreated")
    const supabase = createClient()
    const [userKeys, setUserKeys] = useState<any[]>([])
    const {toast} = useToast()
    const [searchTerm, setSearchTerm] = useState("");

    const filteredKeys = userKeys.filter((key) =>
        key.api.name.toLowerCase().includes(searchTerm.toLowerCase())
    );

    useEffect(() => {
        if (newKeyCreated && newKeyCreated === "success") {
            showNewKeyToast()
        }
    }, [newKeyCreated]);

    useEffect(() => {
        async function fetchKeys() {
            const {data: {user},} = await supabase.auth.getUser();

            const {data, error} = await supabase.from("user_keys").select(
                `
                *,
                api:available_apis ( id, name, endpoint)
                `
            ).eq("user_id", user!.id)

            console.log(data)
            if (error) {
                console.error(error)
            } else {
                setUserKeys(data)
            }
        }

        fetchKeys()

        console.log("Keys", userKeys)
    }, []);

    function showNewKeyToast() {
        console.log("showNewKeyToast")
        return toast({
            title: "API Key created",
            description: "Your new API key has been created successfully",
        })
    }

    return (
        <div className="py-4">
            <h1 className={"text-2xl font-bold"}>Your keys</h1>
            <div className="my-4">
                <div className="relative flex">
                    <SearchIcon
                        className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-gray-500 dark:text-gray-400"/>
                    <Input
                        className="w-full rounded-md border border-gray-300 bg-white px-10 py-2 text-sm shadow-sm transition-colors focus:border-gray-500 focus:outline-none focus:ring-1 focus:ring-gray-500 dark:border-gray-700 dark:bg-gray-950 dark:text-gray-50 dark:focus:border-gray-600 dark:focus:ring-gray-600"
                        placeholder="Search API keys..."
                        type="search"
                        value={searchTerm}
                        onChange={(e) => setSearchTerm(e.target.value)}
                    />
                    <div>
                        <Link href={"/dashboard/keys/new"}>
                            <Button
                                className="ml-2"
                                size="sm">
                                Create API Key
                            </Button>
                        </Link>
                    </div>
                </div>
            </div>
            <div className="overflow-x-auto">
                <Table className={"table-fixed"}>
                    <TableHeader>
                        <TableRow>
                            <TableHead style={{ width: '20%' }}>Key Name</TableHead>
                            <TableHead style={{ width: '30%' }}>URL</TableHead>
                            <TableHead style={{ width: '10%' }}>Key</TableHead>
                            <TableHead style={{ width: '10%' }}>Created at</TableHead>
                            <TableHead style={{ width: '10%' }}>Last Used at</TableHead>
                            <TableHead style={{ width: '10%' }}>Expires at</TableHead>
                            <TableHead style={{ width: '10%' }} className={"text-right"}>Actions</TableHead>
                        </TableRow>
                    </TableHeader>
                    <TableBody>
                        {
                            filteredKeys.length > 0 ? (
                                filteredKeys.map((keyProps, index) => {
                                    return <KeysTableRow key={index} keyProps={keyProps}/>
                                })
                            ) : (
                                <tr>
                                    <td colSpan={7} className="text-center py-4">No keys found</td>
                                </tr>
                            )
                        }
                    </TableBody>
                </Table>
            </div>
            <Toaster/>
        </div>
    )
}

const defaultKeys: IKeys[] = [
    {
        id: "1",
        name: "API Key 1",
        key: "abc123",
        api_url: "https://api.example.com",
        created: "2023-04-15",
        lastUsed: "2023-05-01",
    },
    {
        id: "2",
        name: "API Key 2",
        key: "def456",
        api_url: "https://api.example.com",
        created: "2023-03-20",
        lastUsed: "2023-04-25",
    },
    {
        id: "3",
        name: "API Key 3",
        key: "ghi789",
        api_url: "https://api.example.com",
        created: "2023-02-10",
        lastUsed: "2023-03-15",
    },
]