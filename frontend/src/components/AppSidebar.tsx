import { Link } from "react-router-dom";
import { Layers, FileQuestionMark, Settings, SquarePen, Menu } from "lucide-react";

import {
  Sidebar,
  SidebarHeader,
  SidebarContent,
  SidebarTrigger,
  SidebarGroup,
  SidebarGroupContent,
  SidebarGroupLabel,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
} from "@/components/ui/sidebar";

// Menu items.
const items = [
  {
    title: "New Exam",
    url: "/instructor/exams/new",
    icon: SquarePen,
  },
  {
    title: "My Exams",
    url: "/instructor/exams",
    icon: Layers,
  },
  {
    title: "Questions",
    url: "/instructor/exams/:examId/questions",
    icon: FileQuestionMark,
  },
];

export function AppSidebar() {
  return (
    <Sidebar>
      <SidebarContent>
        <SidebarHeader>
          <Link to="/instructor/dashboard">
            <img
              src="/tAhIni-logo.png"
              alt="tahini-logo"
              className="h-[40px] w-[40px]"
            />
          </Link>
        </SidebarHeader>
        <SidebarGroup>
          <SidebarGroupLabel>Instructor Panel</SidebarGroupLabel>
          <SidebarTrigger>
            <Menu className="h-5 w-5" />
          </SidebarTrigger>
          <SidebarGroupContent>
            <SidebarMenu>
              {items.map((item) => {
                const Icon = item.icon;

                return (
                  <SidebarMenuItem key={item.title}>
                    <SidebarMenuButton
                      asChild
                      className="group-hover:bg-accent"
                    >
                      <Link to={item.url} className="flex w-full items-center gap-2">
                        <Icon className="!h-5 !w-5" name={item.title}/>
                        <span>{item.title}</span>
                      </Link>
                    </SidebarMenuButton>
                  </SidebarMenuItem>
                );
              })}
            </SidebarMenu>
          </SidebarGroupContent>
        </SidebarGroup>
      </SidebarContent>
    </Sidebar>
  );
}
