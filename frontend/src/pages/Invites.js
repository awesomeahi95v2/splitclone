import { useEffect, useState } from "react";
import { useAuth } from "../context/AuthContext";
import { getInvites, acceptInvite } from "../api/api";

function Invites() {
  const { user } = useAuth();
  const [invites, setInvites] = useState([]);

  useEffect(() => {
    getInvites(user.id).then(setInvites).catch(console.error);
  }, [user]);

  const handleRespond = async (groupId, accept) => {
    try {
      await acceptInvite(user.id, groupId, accept);
      setInvites(invites.filter((i) => i.group_id !== groupId));
    } catch (err) {
      alert("Failed to respond to invite");
    }
  };

  return (
    <div>
      <h1>Your Invites</h1>
      {invites.length === 0 ? (
        <p>No pending invites</p>
      ) : (
        <ul>
          {invites.map((invite) => (
            <li key={invite.group_id}>
              {invite.group_name}
              <button onClick={() => handleRespond(invite.group_id, true)}>Accept</button>
              <button onClick={() => handleRespond(invite.group_id, false)}>Decline</button>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

export default Invites;
