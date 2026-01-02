import { User } from "../types/auth";
import { useEffect, useCallback, useState, ReactNode } from "react";
import { AuthContext } from "./AuthContext";
import { jwtDecode } from "jwt-decode";

interface AuthProviderProps {
  children: ReactNode;
}

export const AuthProvider = ({ children }: AuthProviderProps) => {
  const [user, setUser] = useState<User | null>(null);
  const [token, setToken] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

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
          // Check if token is expired
          const decoded = jwtDecode<{ exp: number }>(storedToken);
          const currentTime = Date.now() / 1000;

          if (decoded.exp < currentTime) {
            console.warn("Token expired, logging out.");
            logout();
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

    // Listen for 'unauthorized' events from your API service
    window.addEventListener("auth-unauthorized", logout);
    return () => window.removeEventListener("auth-unauthorized", logout);
  }, []);

  const login = (userData: any, token: string) => {
    localStorage.setItem("tAhIni_token", token);
    localStorage.setItem("tAhIni_user", JSON.stringify(userData));
    setUser(userData);
    setToken(token);

    const decoded = jwtDecode<{ exp: number }>(token);
    const delay = decoded.exp * 1000 - Date.now();

    setTimeout(() => {
      logout();
      alert("Your session has expired. Please log in again.");
    }, delay);
  };

  return (
    <AuthContext.Provider value={{ user, token, login, logout, loading }}>
      {children}
    </AuthContext.Provider>
  );
};
