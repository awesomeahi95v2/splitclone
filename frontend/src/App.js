import React from "react";
import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
import { useAuth } from "./context/AuthContext";
import { useLocation } from "react-router-dom";

import Navbar from "./components/Navbar";
import Login from "./pages/Login";
import GroupsList from "./pages/GroupsList";
import GroupDetails from "./pages/GroupDetails";
import AddEditGroup from "./pages/AddEditGroup";
import AddEditExpense from "./pages/AddEditExpense";
import SettleUp from "./pages/SettleUp";
import RequireAuth from "./components/RequireAuth";
import Invites from "./pages/Invites";

function AddEditExpenseWrapper() {
  const location = useLocation();
  const members = location.state?.members || [];

  return <AddEditExpense members={members} />;
}


function App() {
  const { user } = useAuth();

  return (
    <Router>
      {user && <Navbar />}
      <Routes>
        {/* Login route only if not logged in */}
        {!user && <Route path="/" element={<Login />} />}
        
        {/* Redirect logged in users from "/" to "/groups" */}
        {user && <Route path="/" element={<Navigate to="/groups" />} />}

        {/* All protected routes */}
        <Route path="/groups" element={<RequireAuth><GroupsList /></RequireAuth>} />
        <Route path="/groups/new" element={<RequireAuth><AddEditGroup /></RequireAuth>} />
        <Route path="/groups/:id" element={<RequireAuth><GroupDetails /></RequireAuth>} />
        <Route path="/groups/:id/settle-up" element={<RequireAuth><SettleUp /></RequireAuth>} />
        <Route path="/invites" element={<RequireAuth><Invites /></RequireAuth>} />
        <Route path="/groups/:id/add-expense" element={<RequireAuth><AddEditExpenseWrapper /></RequireAuth>} />

        {/* Redirect any unknown routes */}
        <Route path="*" element={<Navigate to={user ? "/groups" : "/"} />} />
      </Routes>
    </Router>
  );
}

export default App;
