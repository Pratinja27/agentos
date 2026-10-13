async function request(path, options = {}) {
  const response = await fetch(path, {
    headers: { "Content-Type": "application/json", ...(options.headers || {}) },
    ...options,
  });
  if (!response.ok) {
    throw new Error(await response.text());
  }
  return response.json();
}

export const api = {
  overview: () => request("/api/overview"),
  goals: () => request("/api/goals"),
  goal: (id) => request(`/api/goals/${id}`),
  createGoal: (body) => request("/api/goals", { method: "POST", body: JSON.stringify(body) }),
  replan: (id) => request(`/api/goals/${id}/replan`, { method: "POST" }),
  schedule: () => request("/api/schedule"),
  approvals: () => request("/api/approvals"),
  decide: (id, decision) => request(`/api/approvals/${id}/${decision}`, { method: "POST" }),
  memory: () => request("/api/memory"),
  addMemory: (body) => request("/api/memory", { method: "POST", body: JSON.stringify(body) }),
};
