const BASE_URL = "http://splitclone-alb-905942501.us-east-1.elb.amazonaws.com";

// Group APIs
export async function createGroup(data) {
  const response = await fetch(`${BASE_URL}/groups/create`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  if (!response.ok) throw new Error("Failed to create group");
  return await response.json();
}

export async function getGroups(userId) {
  const response = await fetch(`${BASE_URL}/groups/user/${userId}`);
  if (!response.ok) throw new Error("Failed to fetch groups");
  return await response.json();
}

export async function getGroupDetails(groupId) {
  const response = await fetch(`${BASE_URL}/groups/${groupId}`);
  if (!response.ok) throw new Error("Failed to fetch group details");
  return await response.json();
}

// Expense APIs
export async function addExpense(groupId, data) {
  const response = await fetch(`${BASE_URL}/groups/${groupId}/expenses`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  if (!response.ok) throw new Error("Failed to add expense");
  return await response.json();
}

export async function getSettleUp(groupId) {
  const response = await fetch(`${BASE_URL}/groups/${groupId}/settle-up`);
  if (!response.ok) throw new Error("Failed to fetch settle-up info");
  return await response.json();
}

// Auth APIs
export async function signup(email, password) {
  const response = await fetch(`${BASE_URL}/signup`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password }),
  });
  const data = await response.json();
  if (!response.ok) throw new Error(data.error || "Signup failed");
  return data;
}

export async function login(email, password) {
  const response = await fetch(`${BASE_URL}/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password }),
  });
  const data = await response.json();
  if (!response.ok) throw new Error(data.error || "Login failed");
  return data;
}

// Invite APIs
export async function getInvites(userId) {
  const res = await fetch(`${BASE_URL}/users/${userId}/invites`);
  if (!res.ok) throw new Error("Failed to get invites");
  return await res.json();
}

export async function acceptInvite(userId, groupId, accept = true) {
  const res = await fetch(`${BASE_URL}/groups/${groupId}/respond`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ user_id: userId, accept }),
  });
  if (!res.ok) throw new Error("Failed to respond to invite");
  return await res.json();
}

export async function inviteUser(groupId, email) {
  const res = await fetch(`${BASE_URL}/groups/${groupId}/invite`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email }),
  });
  if (!res.ok) throw new Error("Failed to invite user");
  return await res.json();
}
