import {Button} from "@/components/ui/button";
import {SearchIcon} from "lucide-react";
import {Input} from "@/components/ui/input";
import {Table, TableBody, TableCell, TableHead, TableHeader, TableRow} from "@/components/ui/table";
import KeysTableRow from "@/components/keys/TableRow";
import Link from "next/link";

export interface IKeys {
    id: string;
    name: string;
    key: string;
    api_url: string;
    created: string;
    lastUsed: string;
}

export default async function Page() {
    // const {data: todos} = await supabaseClient.from('todos').select()
    const keys = defaultKeys

    return (
        <div className="py-4">
            <div className="mb-6">
                <div className="relative flex">
                    <SearchIcon
                        className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-gray-500 dark:text-gray-400"/>
                    <Input
                        className="w-full rounded-md border border-gray-300 bg-white px-10 py-2 text-sm shadow-sm transition-colors focus:border-gray-500 focus:outline-none focus:ring-1 focus:ring-gray-500 dark:border-gray-700 dark:bg-gray-950 dark:text-gray-50 dark:focus:border-gray-600 dark:focus:ring-gray-600"
                        placeholder="Search API keys..."
                        type="search"
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
                <Table>
                    <TableHeader>
                        <TableRow>
                            <TableHead>Key Name</TableHead>
                            <TableHead>Created</TableHead>
                            <TableHead>Last Used</TableHead>
                            <TableHead>API Url</TableHead>
                            <TableHead className={"text-right"}>Actions</TableHead>
                        </TableRow>
                    </TableHeader>
                    <TableBody>
                        {
                            keys.map((keyProps, index) => {
                                return <KeysTableRow key={index} keyProps={keyProps}/>
                            })
                        }
                    </TableBody>
                </Table>
            </div>
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