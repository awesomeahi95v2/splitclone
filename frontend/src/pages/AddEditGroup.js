import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import { createGroup } from "../api/api";

function AddEditGroup() {
  const [name, setName] = useState("");
  const [error, setError] = useState("");
  const { user } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!name.trim()) return setError("Group name is required");

    try {
      await createGroup({ name, user_id: user.id });
      navigate("/groups");
    } catch (err) {
      console.error(err);
      setError("Failed to create group");
    }
  };

  return (
    <div>
      <h1>Create a New Group</h1>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="Enter group name"
          value={name}
          onChange={(e) => setName(e.target.value)}
        />
        <button type="submit">Create Group</button>
      </form>
      {error && <p style={{ color: "red" }}>{error}</p>}
      <br />
      <button onClick={() => navigate("/groups")}>← Back</button>
    </div>
  );
}

export default AddEditGroup;
