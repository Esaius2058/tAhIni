import { Outlet, useNavigate } from "react-router-dom";
import { SidebarProvider } from "./ui/sidebar";
import { AppSidebar } from "./AppSidebar";
import { useAuth } from "../auth/useAuth";
import { toast } from "sonner";
import { ExamProvider } from "../context/ExamContext"; 

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
          {/* 2. Wrap the Outlet. Now every page inside Outlet can use useExams() */}
          {/* Ensure user.id exists before passing it, or handle null inside the provider */}
          {user?.id && (
            <ExamProvider instructorId={user.id}>
               <Outlet />
            </ExamProvider>
          )}
          
          {/* Fallback if user is loading/undefined (optional) */}
          {!user?.id && <Outlet />}
        </main>
      </div>
    </SidebarProvider>
  );
}