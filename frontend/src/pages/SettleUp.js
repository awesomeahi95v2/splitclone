import { useState } from "react";
import { useParams } from "react-router-dom";
import { getSettleUp } from "../api/api";

function SettleUp() {
  const { id: groupId } = useParams();
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleSettleUp = async () => {
    setLoading(true);
    try {
      const res = await getSettleUp(groupId);
      setResults(res);
    } catch (err) {
      console.error("Settle up failed", err);
      alert("Failed to fetch settlement results.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <h2>Settle Up</h2>
      <button onClick={handleSettleUp} disabled={loading}>
        {loading ? "Calculating..." : "Settle Up"}
      </button>
      <ul>
        {results.length === 0 && !loading && <p>No settlement needed.</p>}
        {results.map((tx, i) => (
          <li key={i}>
            {tx.from} → {tx.to}: £{tx.amount}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default SettleUp;
