import { Link } from "react-router-dom";

function Home() {
  return (
    <div>
      <h1>Home Page</h1>
      <ul>
        <li><Link to="/groups">View All Groups</Link></li>
        <li><Link to="/groups/1">Go to Group 1 Details</Link></li>
        <li><Link to="/groups/1/edit">Edit Group 1</Link></li>
        <li><Link to="/groups/1/add-expense">Add Expense to Group 1</Link></li>
        <li><Link to="/groups/1/settle-up">Settle Up Group 1</Link></li>
      </ul>
    </div>
  );
}

export default Home;
