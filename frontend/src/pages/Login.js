import { useNavigate } from "react-router-dom";
import { useState } from "react";
import { useAuth } from "../context/AuthContext";
import { login, signup } from "../api/api";

function Login() {
  const { setUser } = useAuth();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [isSignup, setIsSignup] = useState(false);
  const navigate = useNavigate();

  const handleAuth = async () => {
    try {
      const userData = isSignup
        ? await signup(email, password)
        : await login(email, password);

      setUser({ email: userData.email, id: userData.id });
      navigate("/groups");
    } catch (err) {
      alert(err.message || "Something went wrong");
    }
  };

  return (
    <div>
      <h1>{isSignup ? "Sign Up" : "Login"}</h1>
      <input
        type="email"
        placeholder="Enter your email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
      />
      <br />
      <input
        type="password"
        placeholder="Enter your password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
      />
      <br />
      <button onClick={handleAuth}>{isSignup ? "Sign Up" : "Login"}</button>
      <br />
      <button onClick={() => setIsSignup(!isSignup)}>
        {isSignup ? "Already have an account? Log in" : "No account? Sign up"}
      </button>
    </div>
  );
}

export default Login;
