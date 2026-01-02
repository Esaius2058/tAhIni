import { User } from "../types/auth";
import {
  createContext,
  useContext,
} from "react";

interface AuthContextType {
  user: User | null;
  token: string | null; 
  login: (userData: any, token: string) => void;
  logout: () => void;
  loading: boolean;
}

export const AuthContext = createContext<AuthContextType | undefined>(
  undefined
);

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
}
