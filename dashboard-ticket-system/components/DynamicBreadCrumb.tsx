"use client"

import {usePathname} from 'next/navigation';
import Link from 'next/link';
import {Fragment} from "react";
import {
    Breadcrumb,
    BreadcrumbItem,
    BreadcrumbLink,
    BreadcrumbList,
    BreadcrumbSeparator
} from "@/components/ui/breadcrumb"; // Replace with your actual imports

const DynamicBreadcrumb = () => {
    const path = usePathname()
    const breadcrumbs = parsePath(path);

    return (
        <Breadcrumb className="hidden md:flex">
            <BreadcrumbList>
                {breadcrumbs.map((crumb, index) => (
                    <Fragment key={index}>
                        <BreadcrumbItem>
                            {index < breadcrumbs.length - 1 ? (
                                <BreadcrumbLink asChild>
                                    <Link href={crumb.href}>{crumb.name}</Link>
                                </BreadcrumbLink>
                            ) : (
                                <span>{crumb.name}</span>  // Non-clickable for the current page
                            )}
                        </BreadcrumbItem>
                        {index < breadcrumbs.length - 1 && <BreadcrumbSeparator />}
                    </Fragment>
                ))}
            </BreadcrumbList>
        </Breadcrumb>
    );
};

const parsePath = (path: string) => {
    const paths = path.split('/').filter(p => p);
    return paths.map((p, index) => ({
        name: p.replace(/-/g, ' ').charAt(0).toUpperCase() + p.replace(/-/g, ' ').slice(1),  // Replace hyphens, capitalize
        href: '/' + paths.slice(0, index + 1).join('/')  // Construct URL up to the current crumb
    }));
};

export default DynamicBreadcrumb;
