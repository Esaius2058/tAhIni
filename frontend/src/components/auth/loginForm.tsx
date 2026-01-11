import { useState } from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { toast } from "sonner";
import { loginSchema } from "../../forms/auth/login.schema";
import { LoginFormValues } from "../../forms/auth/login.types";
import { loginUserApi } from "../../api/auth";
import { useAuth } from "../../auth/useAuth";
import { Spinner } from "../ui/spinner";
import { useAutoDismissErrors } from "../../hooks/useAutoDismissErrors";

interface LoginFormProps {
  onSuccess: (role?: string) => void;
}

export function LoginForm({ onSuccess }: LoginFormProps) {
  const [loading, setLoading] = useState(false);
  const { login } = useAuth();

  const form = useForm<LoginFormValues>({
    resolver: zodResolver(loginSchema),
  });

  useAutoDismissErrors(form);

  const { register, handleSubmit, formState: { errors } } = form;

  const onSubmit = async (data: LoginFormValues) => {
    try {
      setLoading(true);
      const res = await loginUserApi(data, login);
      toast.success("Logged in successfully");
      onSuccess(res.user?.type); // Tell parent we are done
    } catch (err: any) {
      const msg = err.response?.data?.detail || "Login failed";
      toast.error(msg);
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="form-card">
      <div>
        <input
          type="email"
          placeholder="you@example.com"
          {...register("email")}
          className={errors.email ? "border-red-500" : ""}
        />
        {errors.email && (
          <p className="text-xs text-red-500 mt-1">{errors.email.message}</p>
        )}
      </div>

      <div>
        <input
          type="password"
          placeholder="Password"
          {...register("password")}
          className={errors.password ? "border-red-500" : ""}
        />
        {errors.password && (
          <p className="text-xs text-red-500 mt-1">{errors.password.message}</p>
        )}
      </div>

      <button type="submit" disabled={loading}>
        {loading ? <Spinner /> : "Log In"}
      </button>
    </form>
  );
}