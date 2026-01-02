import { useState } from "react";
import { Outlet, useNavigate } from "react-router-dom";
import { SidebarProvider } from "./ui/sidebar";
import { AppSidebar } from "./AppSidebar";
import { useAuth } from "../auth/useAuth";
import { toast } from "sonner"

export default function Layout() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    toast.success("Logged out successfully");
    navigate("/login");
  };

  return (
    <SidebarProvider>
      <AppSidebar />
      <div className="w-full p-0">
        <header className="h-16 w-full bg-white flex items-center justify-between px-4">
          <div className="font-semibold">
            Welcome, {user?.name || "Instructor"}
          </div>

          <button
            className="px-3 py-1 "
            onClick={handleLogout}
          >
            Logout
          </button>
        </header>

        <main className="flex-1 overflow-y-auto p-6">
          <Outlet />
        </main>
      </div>
    </SidebarProvider>
  );
}
