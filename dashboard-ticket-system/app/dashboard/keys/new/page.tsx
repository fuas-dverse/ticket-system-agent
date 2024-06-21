"use client"
import {zodResolver} from "@hookform/resolvers/zod"
import {useForm} from "react-hook-form"
import {z} from "zod"
import {
    Form,
    FormControl,
    FormDescription,
    FormField,
    FormItem,
    FormLabel,
    FormMessage,
} from "@/components/ui/form"
import {cn} from "@/lib/utils"
import {Button} from "@/components/ui/button"
import {
    Command,
    CommandEmpty,
    CommandGroup,
    CommandInput,
    CommandItem,
} from "@/components/ui/command"
import {
    Popover,
    PopoverContent,
    PopoverTrigger,
} from "@/components/ui/popover"
import {Check, ChevronsUpDown, CircleCheck, CircleX} from "lucide-react"
import {useEffect, useLayoutEffect, useRef, useState} from "react";
import {createClient} from "@/utils/supabase/client";
import {Card, CardContent, CardHeader, CardTitle} from "@/components/ui/card";
import Link from "next/link";
import {useRouter} from "next/navigation";

const formSchema = z.object({
    api: z.number({
        required_error: "API is required.",
    }),
})

export default function Page() {
    const [availableAPIS, setAvailableAPIS] = useState<any[]>([])
    const dropdownRef = useRef<HTMLButtonElement>(null);
    const [buttonWidth, setButtonWidth] = useState(0);
    const supabase = createClient()
    const [selectedAPI, setSelectedAPI] = useState<any>(0)
    const router = useRouter()
    const form = useForm<z.infer<typeof formSchema>>({
        resolver: zodResolver(formSchema),
    })

    async function fetchAvailableAPIs() {
        const {data, error} = await supabase.from("available_apis").select()
        if (error) {
            console.error(error)
            return
        }
        setAvailableAPIS(data)
    }

    useEffect(() => {
        fetchAvailableAPIs()
    }, [fetchAvailableAPIs])


    useLayoutEffect(() => {
        const updateWidth = () => {
            if (dropdownRef.current) {
                setButtonWidth(dropdownRef.current.offsetWidth);
            }
        };

        updateWidth(); // Update width on mount and layout changes
        window.addEventListener('resize', updateWidth); // Update width on window resize

        return () => window.removeEventListener('resize', updateWidth);
    }, []);

    useEffect(() => {
        const apiId = form.watch("api");
        const selected = availableAPIS.find(api => api.id === apiId);
        setSelectedAPI(selected);
    }, [availableAPIS, form.watch("api")]);


    async function onSubmit() {

        const { data: {user},} = await supabase.auth.getUser();

        const {data, error} = await supabase.from("user_keys").insert({
            user_id: user!.id,
            api_id: form.getValues("api"),
            expires_at: new Date(new Date().getTime() + 1000 * 60 * 60 * 24 * 30 * 365),
        })

        if (error) {
            console.error(error)
            return
        }

        router.push("/dashboard/keys?newKeyCreated=success")
    }

    return (
        <section className="flex flex-col md:flex-row items-start gap-8 my-4">
            <div className={"flex-1"}>
                <h1 className={"text-2xl font-bold"}>Generate a new Key</h1>
                <div className={"my-4"}>
                    <Form {...form}>
                        <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-8">
                            <FormField
                                control={form.control}
                                name="api"
                                render={({field}) => (
                                    <FormItem className="flex flex-col">
                                        <FormLabel>Available API&apos;s</FormLabel>
                                        <Popover>
                                            <PopoverTrigger asChild>
                                                <FormControl>
                                                    <Button
                                                        ref={dropdownRef}
                                                        variant="outline"
                                                        role="combobox"
                                                        className={cn(
                                                            "justify-between",
                                                            !field.value && "text-muted-foreground"
                                                        )}
                                                    >
                                                        {field.value
                                                            ? availableAPIS.find(
                                                                (api) => api.id === field.value
                                                            )?.name
                                                            : "Select API"}
                                                        <ChevronsUpDown className="ml-2 h-4 w-4 shrink-0 text-primary"/>
                                                    </Button>
                                                </FormControl>
                                            </PopoverTrigger>
                                            <PopoverContent style={{width: `${buttonWidth}px`, padding: 0}}>
                                                <Command>
                                                    <CommandInput placeholder="Search api..."/>
                                                    <CommandEmpty>No API found.</CommandEmpty>
                                                    <CommandGroup>
                                                        {availableAPIS.map((api, index) => (
                                                            <CommandItem
                                                                value={api.name}
                                                                key={index}
                                                                onSelect={() => {
                                                                    form.setValue("api", api.id)
                                                                }}
                                                            >
                                                                <Check
                                                                    className={cn(
                                                                        "mr-2 h-4 w-4 text-primary",
                                                                        api.id === field.value
                                                                            ? "opacity-100"
                                                                            : "opacity-0"
                                                                    )}
                                                                />
                                                                {api.name}
                                                            </CommandItem>
                                                        ))}
                                                    </CommandGroup>
                                                </Command>
                                            </PopoverContent>
                                        </Popover>
                                        <FormMessage/>
                                    </FormItem>
                                )}
                            />
                            <Button type={"submit"}>Generate Key</Button>
                        </form>
                    </Form>
                </div>
            </div>
            <div className="flex-1">
                <h2 className="text-2xl font-bold">API Overview</h2>
                <div className="grid gap-4 my-4">
                    {selectedAPI ? (
                        <Card>
                            <CardHeader>
                                <CardTitle>{selectedAPI.name}</CardTitle>
                            </CardHeader>
                            <CardContent>
                                <div className="grid gap-4">
                                    <div className={"max-w-1/2 overflow-auto break-words"}>
                                        <h3 className={"text-xl font-bold"}>Description</h3>
                                        <p>
                                            {selectedAPI.description}
                                        </p>
                                    </div>

                                    <div className={"max-w-1/2 overflow-auto break-words"}>
                                        <h3 className={"text-xl font-bold"}>API Endpoint</h3>
                                        <Link href={selectedAPI.endpoint} className={"text-primary"}>
                                            {selectedAPI.endpoint}
                                        </Link>
                                    </div>

                                    <div>
                                        <h3 className={"text-xl font-bold"}>Documentation</h3>
                                        <Link href={selectedAPI.website} className={"text-primary"}>
                                            {selectedAPI.website}
                                        </Link>
                                    </div>
                                    <div>
                                        <div className={"text-xl font-bold flex flex-row"}>Status
                                            {selectedAPI.status ? <CircleX className={"ml-2 h-7 w-7"} color={"red"}/> :
                                                <CircleCheck className={"ml-4 h-7 w-7 text-primary"}/>}
                                        </div>
                                    </div>
                                </div>
                            </CardContent>
                        </Card>
                    ) : (
                        <p>Select an API to see more details.</p>
                    )}
                </div>
            </div>
        </section>
    )
}
