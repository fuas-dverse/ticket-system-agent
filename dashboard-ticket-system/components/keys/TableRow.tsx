"use client"
import {TableCell, TableRow} from "@/components/ui/table";
import {CopyIcon, KeyIcon, Settings} from "lucide-react";
import {DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuTrigger} from "@/components/ui/dropdown-menu";
import {Button} from "@/components/ui/button";
import {toast} from "@/components/ui/use-toast";
import {createClient} from "@/utils/supabase/client";
import {revalidatePath} from "next/cache";

interface Props {
    keyProps: any
    onDelete: (keyId: string) => void;
}

export default function KeysTableRow({keyProps, onDelete}: Props) {
    const createdAt = new Date(keyProps.created_at).toISOString().split('T')[0]
    const updatedAt = new Date(keyProps.updated_at).toISOString().split('T')[0]
    const expiresAt = new Date(keyProps.expires_at).toISOString().split('T')[0]
    const supabase = createClient()

    async function deleteKey() {
        const { error } = await supabase.from("user_keys").delete().eq("id", keyProps.id);

        if (error) {
            console.error(error);
        } else {
            onDelete(keyProps.id);
            toast({
                title: "Key Deleted",
                description: "The key has been deleted successfully"
            });
        }
    }

    return (
        <TableRow className={"relative w-full"}>
            <TableCell className="">
                <div className="flex items-center gap-2">
                    <KeyIcon className="h-5 w-5 text-gray-500 dark:text-gray-400"/>
                    <span>{keyProps.api.name}</span>
                </div>
            </TableCell>

            <TableCell className={""}>
                <div className={"hover:cursor-pointer"} onClick={() => {
                    // function to copy the text to clipboard
                    navigator.clipboard.writeText(keyProps.api.endpoint);
                    toast({
                        title: "URL Copied to clipboard",
                    })
                }}>
                    {keyProps.api.endpoint.substring(0, 20)}
                    ...
                    {keyProps.api.endpoint.substring(keyProps.api.endpoint.length - 10, keyProps.api.endpoint.length)}

                </div>
            </TableCell>
            <TableCell className={""}>
                <div className={"flex"}>
                    ******
                    <CopyIcon
                        className="h-5 w-5 ml-2 text-gray-500 dark:text-gray-400 hover:cursor-pointer"
                        onClick={() => {
                            navigator.clipboard.writeText(keyProps.key);
                            toast({
                                title: "Key Copied to clipboard",
                            })
                        }}
                    />
                </div>
            </TableCell>
            <TableCell className={""}>{createdAt.toString()}</TableCell>
            <TableCell className={""}>{updatedAt.toString()}</TableCell>
            <TableCell className={""}>{expiresAt.toString()}</TableCell>
            <TableCell className="text-right ">
                <DropdownMenu>
                    <DropdownMenuTrigger asChild>
                        <Button size="icon" variant="ghost">
                            <Settings className="h-5 w-5"/>
                            <span className="sr-only">More actions</span>
                        </Button>
                    </DropdownMenuTrigger>
                    <DropdownMenuContent align="end">
                        <DropdownMenuItem onClick={deleteKey} className={"text-red-500"}>Delete</DropdownMenuItem>
                    </DropdownMenuContent>
                </DropdownMenu>
            </TableCell>
        </TableRow>
    )
}