import { useEffect, useState } from "react";
import { useParams, useNavigate, Link } from "react-router-dom";
import { getGroupDetails, getSettleUp, inviteUser } from "../api/api";
import { useAuth } from "../context/AuthContext";

function GroupDetails() {
  const { id } = useParams();
  const { user } = useAuth();
  const navigate = useNavigate();

  const [group, setGroup] = useState(null);
  const [settleUp, setSettleUp] = useState([]);
  const [inviteEmail, setInviteEmail] = useState("");
  const [error, setError] = useState("");

  useEffect(() => {
  getGroupDetails(id)
    .then(res => {
      console.log("group details", res);
      setGroup(res);
    })
    .catch(console.error);

  getSettleUp(id)
    .then(settle => {
      setSettleUp(settle);
    })
    .catch(console.error);
}, [id]);


  const handleInvite = async () => {
    try {
      await inviteUser(id, inviteEmail);
      alert("User invited!");
      setInviteEmail("");
    } catch (err) {
      setError("Failed to invite user");
    }
  };

  const getEmailById = (uid) => group.members.find(m => m.id === uid)?.email || uid;

  if (!group) return <p>Loading...</p>;

  return (
    <div>
      <h1>{group.name}</h1>

      <h2>Members</h2>
      <ul>
        {group.members.map((m) => (
          <li key={m.id}>{m.email}</li>
        ))}
      </ul>

      <h2>Expenses</h2>
      <button onClick={() => navigate(`/groups/${id}/add-expense`, { state: { members: group.members } })}>
        + Add Expense
      </button>
      <table border="1" cellPadding="8" style={{ marginTop: "10px", width: "100%" }}>
        <thead>
          <tr>
            <th>Description</th>
            <th>Amount</th>
            <th>Currency</th>
            <th>Paid By</th>
            <th>Members Involved</th>
            <th>Outcome</th>
          </tr>
        </thead>
        <tbody>
          {group.expenses.map((exp) => {
            const splits = exp.splits || [];
            const payerEmail = getEmailById(exp.paid_by);
            const involvedIds = splits.map(s => s.user_id);
            const involvedEmails = involvedIds.map(getEmailById).join(", ");
            const isUserInvolved = involvedIds.includes(user.id);
            const yourSplit = splits.find(s => s.user_id === user.id);
            let outcome = "You are not involved";
            let bgColor = "#eee";

            if (user.id === exp.paid_by) {
              const owedUsers = splits.filter(s => s.user_id !== user.id);
              if (owedUsers.length > 0) {
                const names = owedUsers.map(s => getEmailById(s.user_id));
                const total = owedUsers.reduce((sum, s) => sum + s.amount, 0);
                outcome = `${names.join(", ")} owe you £${total.toFixed(2)}`;
                bgColor = "#d4edda";
              }
            } else if (yourSplit) {
              outcome = `You owe ${payerEmail} £${yourSplit.amount.toFixed(2)}`;
              bgColor = "#f8d7da";
            }

            return (
              <tr key={exp.id} style={{ backgroundColor: bgColor }}>
                <td>{exp.description}</td>
                <td>£{exp.amount.toFixed(2)}</td>
                <td>{exp.currency}</td>
                <td>{payerEmail}</td>
                <td>{involvedEmails}</td>
                <td>{outcome}</td>
              </tr>
            );
          })}
        </tbody>
      </table>

      <h2>Settle Up</h2>
      <ul>
        {settleUp.length === 0 ? (
          <li>No outstanding balances</li>
        ) : (
          settleUp
            .filter(tx => tx.from === user.id || tx.to === user.id)
            .map((tx, i) => {
              const from = getEmailById(tx.from);
              const to = getEmailById(tx.to);
              return (
                <li key={i}>
                  {tx.from === user.id
                    ? `You pay ${to} £${tx.amount.toFixed(2)}`
                    : `${from} pays you £${tx.amount.toFixed(2)}`}
                </li>
              );
            })
        )}
      </ul>

      <h2>Invite User</h2>
      <input
        type="email"
        placeholder="Friend's email"
        value={inviteEmail}
        onChange={(e) => setInviteEmail(e.target.value)}
      />
      <button onClick={handleInvite}>Invite User</button>

      {error && <p style={{ color: "red" }}>{error}</p>}
      <br />
      <Link to="/groups">&#8592; Back to Groups</Link>
    </div>
  );
}

export default GroupDetails;
