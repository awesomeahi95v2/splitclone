import { Navigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

function RequireAuth({ children }) {
  const { user } = useAuth();
  return user ? children : <Navigate to="/" />;
}

export default RequireAuth;
