const links = [
  ["dashboard", "Home"],
  ["goals", "Goals"],
  ["schedule", "Schedule"],
  ["agents", "Agents"],
  ["memory", "Memory"],
  ["approvals", "Approvals"],
];

export default function Layout({ page, setPage, overview, children }) {
  return (
    <div className="min-h-screen flex">
      <aside className="w-64 bg-moss text-paper px-5 py-7 flex flex-col">
        <p className="font-mono text-[11px] tracking-[0.24em] uppercase text-paper/60">Life OS</p>
        <h1 className="font-serif text-3xl mt-2">AgentOS</h1>
        <p className="text-sm text-paper/70 mt-2 leading-6">
          Agentic planning, memory, tools, and human approval.
        </p>
        <nav className="mt-8 space-y-1">
          {links.map(([id, label]) => (
            <button
              key={id}
              onClick={() => setPage(id)}
              className={`w-full text-left px-3 py-2 rounded-lg ${
                page === id ? "bg-paper text-ink" : "text-paper/80 hover:bg-white/10"
              }`}
            >
              {label}
            </button>
          ))}
        </nav>
        <div className="mt-auto text-xs text-paper/60 space-y-1">
          <p>Mode: {overview?.llm_mode || "loading"}</p>
          <p>Pending approvals: {overview?.pending_approvals ?? "-"}</p>
        </div>
      </aside>
      <main className="flex-1 p-8">{children}</main>
    </div>
  );
}
