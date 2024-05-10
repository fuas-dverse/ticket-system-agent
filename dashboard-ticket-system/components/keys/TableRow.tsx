import {TableCell, TableRow} from "@/components/ui/table";
import {KeyIcon, MoveHorizontalIcon} from "lucide-react";
import {DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuTrigger} from "@/components/ui/dropdown-menu";
import {IKeys} from "@/app/dashboard/keys/page";
import {Button} from "@/components/ui/button";

interface Props {
    keyProps: IKeys
}

export default function KeysTableRow({keyProps}: Props) {
    return (
        <TableRow>
            <TableCell className="font-medium">
                <div className="flex items-center gap-2">
                    <KeyIcon className="h-5 w-5 text-gray-500 dark:text-gray-400"/>
                    <span>{keyProps.name}</span>
                </div>
            </TableCell>
            <TableCell>{keyProps.created}</TableCell>
            <TableCell>{keyProps.lastUsed}</TableCell>
            <TableCell>{keyProps.api_url}</TableCell>
            <TableCell className="text-right">
                <DropdownMenu>
                    <DropdownMenuTrigger asChild>
                        <Button size="icon" variant="ghost">
                            <MoveHorizontalIcon className="h-5 w-5"/>
                            <span className="sr-only">More actions</span>
                        </Button>
                    </DropdownMenuTrigger>
                    <DropdownMenuContent align="end">
                        <DropdownMenuItem>View</DropdownMenuItem>
                        <DropdownMenuItem>Regenerate</DropdownMenuItem>
                        <DropdownMenuItem>Delete</DropdownMenuItem>
                    </DropdownMenuContent>
                </DropdownMenu>
            </TableCell>
        </TableRow>
    )
}