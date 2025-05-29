import { useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import { addExpense } from "../api/api";

function AddEditExpense({ members }) {
  const { user } = useAuth();
  const { id: groupId } = useParams();
  const navigate = useNavigate();

  const [description, setDescription] = useState("");
  const [amount, setAmount] = useState("");
  const [paidBy, setPaidBy] = useState(user.id);
  const [selectedMembers, setSelectedMembers] = useState(new Set());
  const [error, setError] = useState("");

  const handleToggleMember = (memberId) => {
    const updated = new Set(selectedMembers);
    if (updated.has(memberId)) {
      updated.delete(memberId);
    } else {
      updated.add(memberId);
    }
    setSelectedMembers(updated);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!description || !amount || selectedMembers.size === 0) {
      return setError("Please fill all fields and select at least one member.");
    }

    const data = {
      description,
      amount: parseFloat(amount),
      currency: "GBP",
      paid_by: paidBy,
      created_by_user_id: user.id,
      involved_members: [...selectedMembers],
    };

    try {
      await addExpense(groupId, data);
      navigate(`/groups/${groupId}`);
    } catch (err) {
      setError("Failed to add expense");
      console.error(err);
    }
  };

  return (
    <div>
      <h2>Add Expense</h2>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="Description"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
        /><br />
        <input
          type="number"
          placeholder="Amount"
          value={amount}
          onChange={(e) => setAmount(e.target.value)}
        /><br />
        <label>
          Paid By:
          <select value={paidBy} onChange={(e) => setPaidBy(e.target.value)}>
            {members.map((m) => (
              <option key={m.id} value={m.id}>{m.email}</option>
            ))}
          </select>
        </label><br />

        <fieldset>
          <legend>Who was involved?</legend>
          {members.map((m) => (
            <label key={m.id}>
              <input
                type="checkbox"
                checked={selectedMembers.has(m.id)}
                onChange={() => handleToggleMember(m.id)}
              />
              {m.email}
            </label>
          ))}
        </fieldset><br />

        <button type="submit">Add Expense</button>
        {error && <p style={{ color: "red" }}>{error}</p>}
      </form>
      <br />
      <button onClick={() => navigate(`/groups/${groupId}`)}>← Back</button>
    </div>
  );
}

export default AddEditExpense;
