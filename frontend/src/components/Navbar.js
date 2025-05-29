import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

function Navbar() {
  const { user, setUser } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    setUser(null);
    navigate("/", { replace: true });
  };

  if (!user) return null;

  return (
    <nav style={{ marginBottom: "20px", padding: "10px", background: "#f0f0f0" }}>
      <span><strong>Logged in as:</strong> {user.email}</span>
      <span style={{ marginLeft: "20px" }}>
        <Link to="/groups">Groups</Link> |{" "}
        <Link to="/invites">Invites</Link>
        <button onClick={handleLogout}>Logout</button>
      </span>
    </nav>
  );
}

export default Navbar;
