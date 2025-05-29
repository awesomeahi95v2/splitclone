import { useEffect, useState } from "react";
import { getGroups } from "../api/api";
import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

function GroupsList() {
  const [groups, setGroups] = useState([]);
  const { user } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    if (user?.id) {
      getGroups(user.id).then(setGroups).catch(console.error);
    }
  }, [user]);

  const handleCreate = () => {
    navigate("/groups/new");
  };

  if (!user) {
    return <p>Loading user info...</p>; // or redirect to login
  }

  return (
    <div>
      <h1>Welcome, {user.email}</h1>
      <button onClick={handleCreate}>+ Create New Group</button>
      <h2>Your Groups</h2>
      {groups.length === 0 ? (
        <p>You are not in any groups yet.</p>
      ) : (
        <ul>
          {groups.map((group) => (
            <li key={group.id}>
              <Link to={`/groups/${group.id}`}>{group.name}</Link>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

export default GroupsList;
