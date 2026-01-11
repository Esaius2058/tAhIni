import { User } from "../types/auth";
import { useEffect, useCallback, useState, ReactNode } from "react";
import { AuthContext } from "./AuthContext";
import { jwtDecode } from "jwt-decode";
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert"; // Import Shadcn Alert
import { AlertCircle, AlertCircleIcon, X } from "lucide-react"; // Import Icons

interface AuthProviderProps {
  children: ReactNode;
}

export const AuthProvider = ({ children }: AuthProviderProps) => {
  const [user, setUser] = useState<User | null>(null);
  const [token, setToken] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);
  
  // 1. Add state to control the visibility of the Alert
  const [sessionExpired, setSessionExpired] = useState(false);

  const logout = useCallback(() => {
    localStorage.removeItem("tAhIni_token");
    localStorage.removeItem("tAhIni_user");
    setUser(null);
    setToken(null);
  }, []);

  useEffect(() => {
    const initializeAuth = () => {
      const storedToken = localStorage.getItem("tAhIni_token");
      const storedUser = localStorage.getItem("tAhIni_user");

      if (storedToken && storedUser) {
        try {
          const decoded = jwtDecode<{ exp: number }>(storedToken);
          const currentTime = Date.now() / 1000;

          if (decoded.exp < currentTime) {
            console.warn("Token expired, logging out.");
            logout();
            // Optional: Show alert if they were logged out on refresh
             setSessionExpired(true); 
          } else {
            setUser(JSON.parse(storedUser));
            setToken(storedToken);
          }
        } catch (error) {
          console.error("Invalid token found:", error);
          logout();
        }
      }
      setLoading(false);
    };

    initializeAuth();

    window.addEventListener("auth-unauthorized", logout);
    return () => window.removeEventListener("auth-unauthorized", logout);
  }, []);

  const login = (userData: any, token: string) => {
    // Reset expiry state on new login
    setSessionExpired(false); 
    
    localStorage.setItem("tAhIni_token", token);
    localStorage.setItem("tAhIni_user", JSON.stringify(userData));
    setUser(userData);
    setToken(token);

    const decoded = jwtDecode<{ exp: number }>(token);
    const delay = decoded.exp * 1000 - Date.now();

    // Set the timer
    setTimeout(() => {
      logout();
      // 2. Instead of alert(), update state to show the component
      setSessionExpired(true); 
    }, delay);
  };

  return (
    <AuthContext.Provider value={{ user, token, login, logout, loading }}>
      
      {/* 3. Conditionally render the Alert fixed at the top of the screen */}
      {sessionExpired && (
        <div className="fixed top-6 left-1/2 -translate-x-1/2 z-[100] w-full max-w-md px-4 animate-in fade-in slide-in-from-top-2">
          <Alert variant="destructive" className="bg-white text-black shadow-lg border-red-200">
            <AlertCircleIcon className="h-4 w-4" />
            <AlertTitle>Session Expired</AlertTitle>
            <AlertDescription className="flex justify-between items-center">
              <span>Your session has timed out. Please log in again.</span>
              
              {/* Close Button */}
              <button 
                onClick={() => setSessionExpired(false)}
                className="ml-4 p-1 bg-transparent text-black hover:bg-red-500 rounded-full transition-colors"
              >
                <X className="h-4 w-4" />
              </button>
            </AlertDescription>
          </Alert>
        </div>
      )}

      {children}
    </AuthContext.Provider>
  );
};