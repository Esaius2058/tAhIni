import { useState } from "react";
import { useForm } from "react-hook-form";
import { useNavigate } from "react-router-dom";
import { zodResolver } from "@hookform/resolvers/zod";
import { loginSchema } from "../forms/auth/login.schema";
import { registerSchema } from "../forms/auth/register.schema";
import { UserType } from "../types/auth";
import { LoginFormValues } from "../forms/auth/login.types";
import { RegisterFormValues } from "../forms/auth/register.types";
import { loginUserApi, registerUserApi } from "../api/auth";
import { Spinner } from "../components/ui/spinner";
import { useAuth } from "../auth/useAuth";
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert";
import { toast } from "sonner";

export default function SignUp() {
  const [formData, setFormData] = useState({
    name: "",
    email: "",
    password: "",
    confirmPassword: "",
  });
  const [loading, setLoading] = useState(false);
  const [authType, setAuthType] = useState<"signup" | "login">("signup");
  const [authHeader, setAuthHeader] = useState<String>("Sign Up");
  const [authPrompt, setAuthPrompt] = useState<String>(
    "Already have an account?"
  );
  const { user, login } = useAuth();
  const navigate = useNavigate();
  const signupFormRef = useForm<RegisterFormValues>({
    resolver: zodResolver(registerSchema),
  });

  const loginFormRef = useForm<LoginFormValues>({
    resolver: zodResolver(loginSchema),
  });

  const roleBasedRedirect = (role: UserType | undefined) => {
    if (role == "admin") {
      navigate("");
    } else if (role == "instructor") {
      navigate("/instructor/dashboard");
    } else {
      navigate("");
    }
  };

  const signupAlert = () => {
    return (
      <Alert variant="default">
        <AlertTitle>Succes!</AlertTitle>
        <AlertDescription>
          Account created successfully. Log in
        </AlertDescription>
      </Alert>
    );
  };

  const signupForm = () => {
    const handleSubmit = async (data: RegisterFormValues) => {
      if (formData.password !== formData.confirmPassword) {
        toast.error("Passwords do not match!");
        return;
      }

      try {
        setLoading(true);
        let response = await registerUserApi(data);
        signupAlert();
        navigate("/");
      } finally {
        setLoading(false);
      }
    };

    return (
      <form
        onSubmit={signupFormRef.handleSubmit(handleSubmit)}
        className="form-card"
      >
        <input
          type="text"
          id="name"
          className=""
          placeholder="John Doe"
          {...signupFormRef.register("name")}
          required
        />
        <input
          type="email"
          id="email"
          className=""
          placeholder="you@example.com"
          {...signupFormRef.register("email")}
          required
        />
        <input
          type="password"
          id="password"
          className=""
          placeholder="password"
          {...signupFormRef.register("password")}
          required
        />
        <input
          type="password"
          id="confirmPassword"
          className=""
          placeholder="confirm password"
          {...signupFormRef.register("password")}
          required
        />
        <button type="submit" disabled={loading}>
          {loading ? <Spinner /> : "Sign Up"}
        </button>
      </form>
    );
  };

  const loginForm = () => {
    const handleSubmit = async (data: LoginFormValues) => {
      try {
        setLoading(true);
        const res = await loginUserApi(data, login);
        console.log("User Type: ", user?.type);
        roleBasedRedirect(res.user?.type);
      } finally {
        setLoading(false);
      }
    };

    return (
      <form
        onSubmit={loginFormRef.handleSubmit(handleSubmit)}
        className="form-card"
      >
        <input
          type="email"
          id="email"
          className=""
          placeholder="you@example.com"
          {...loginFormRef.register("email")}
          required
        />
        <input
          type="password"
          id="password"
          className=""
          placeholder="password"
          {...loginFormRef.register("password")}
          required
        />
        <button type="submit" disabled={loading}>
          {loading ? <Spinner /> : "Log In"}
        </button>
      </form>
    );
  };

  const changeAuthType = (
    e: React.MouseEvent<HTMLAnchorElement, MouseEvent>
  ) => {
    e.preventDefault();
    if (authType === "signup") {
      setAuthType("login");
      setAuthHeader("Log In");
      setAuthPrompt("Don't have an account?");
    } else {
      setAuthType("signup");
      setAuthHeader("Sign Up");
      setAuthPrompt("Already have an account?");
    }
  };

  return (
    <div className="form-container">
      <div>
        <img src="/tAhIni-logo.png" alt="logo" />
        <p>A simple, secure way to take your tests and exams</p>
      </div>
      {authType === "signup" ? signupForm() : loginForm()}
      <div className="">
        <p className="">
          {authPrompt}{" "}
          <a href="#" className="" onClick={changeAuthType}>
            {authHeader === "Sign Up" ? "Log In" : "Sign Up"}
          </a>
        </p>
      </div>
    </div>
  );
}
