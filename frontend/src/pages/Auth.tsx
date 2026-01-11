import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { LoginForm } from "@/components/auth/loginForm";
import { SignUpForm } from "@/components/auth/signUpForm";
import { UserType } from "../types/auth";

export default function AuthPage() {
  const [authType, setAuthType] = useState<"signup" | "login">("signup");
  const navigate = useNavigate();

  const handleLoginSuccess = (role?: string) => {
    if (role === "admin") navigate("/admin");
    else if (role === "instructor") navigate("/instructor/dashboard");
    else navigate("/student/dashboard");
  };

  const handleSignupSuccess = () => {
    setAuthType("login");
  };

  const toggleAuth = (e: React.MouseEvent<HTMLAnchorElement>) => {
    e.preventDefault();
    setAuthType((prev) => (prev === "signup" ? "login" : "signup"));
  };

  return (
    <div className="landing-page">
      <div className="form-container">
        <div 
          className="cursor-pointer hover:opacity-80 transition-opacity" 
          onClick={() => navigate("/")}
        >
          <img
            src="/tAhIniLogoLight.svg"
            alt="logo"
            className="w-32 h-auto" 
          />
        </div>

        {authType === "signup" ? (
          <SignUpForm onSuccess={handleSignupSuccess} />
        ) : (
          <LoginForm onSuccess={handleLoginSuccess} />
        )}

        <div className="mt-4">
          <p>
            {authType === "signup"
              ? "Already have an account?"
              : "Don't have an account?"}{" "}
            <a
              href="#"
              onClick={toggleAuth}
              className="font-bold hover:underline"
            >
              {authType === "signup" ? "Log In" : "Sign Up"}
            </a>
          </p>
        </div>
      </div>
    </div>
  );
}
