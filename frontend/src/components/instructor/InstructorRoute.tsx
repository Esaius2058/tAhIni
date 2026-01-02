// components/InstructorRoute.jsx
import { Navigate } from "react-router-dom";
import { useAuth } from "../../auth/useAuth";

export default function InstructorRoute({ children }) {
  const { user, loading } = useAuth();

  if (loading) return <p>Loading...</p>;

  if (!user) return <Navigate to="/login" />;
  if (user.type !== "instructor") return <Navigate to="/unauthorized" />;

  return children;
}
