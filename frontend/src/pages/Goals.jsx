import { useEffect, useState } from "react";
import { api } from "../api";

const empty = { title: "", description: "", deadline: "", hours_per_day: 4 };

export default function Goals({ onChange }) {
  const [goals, setGoals] = useState([]);
  const [form, setForm] = useState(empty);
  const [busy, setBusy] = useState(false);
  const [open, setOpen] = useState(null);

  async function load() {
    const rows = await api.goals();
    setGoals(rows);
    setOpen(rows[0] || null);
  }

  useEffect(() => {
    load();
  }, []);

  async function submit(event) {
    event.preventDefault();
    setBusy(true);
    try {
      const goal = await api.createGoal(form);
      setForm(empty);
      await load();
      setOpen(goal);
      onChange?.();
    } finally {
      setBusy(false);
    }
  }

  async function replan(id) {
    setBusy(true);
    try {
      const goal = await api.replan(id);
      await load();
      setOpen(goal);
      onChange?.();
    } finally {
      setBusy(false);
    }
  }

  return (
    <div className="grid lg:grid-cols-[1.1fr_0.9fr] gap-6">
      <div>
        <p className="font-mono text-xs uppercase tracking-[0.2em] text-sage">Planner intake</p>
        <h2 className="font-serif text-4xl mt-2">Give AgentOS a goal</h2>
        <form className="card p-6 mt-6 space-y-4" onSubmit={submit}>
          <input
            className="w-full border border-black/10 rounded-xl px-3 py-2 bg-white"
            placeholder="Prepare for exams while keeping gym and work"
            value={form.title}
            onChange={(e) => setForm({ ...form, title: e.target.value })}
            required
          />
          <textarea
            className="w-full border border-black/10 rounded-xl px-3 py-2 bg-white min-h-24"
            placeholder="Constraints, deadlines, things that must not be dropped"
            value={form.description}
            onChange={(e) => setForm({ ...form, description: e.target.value })}
          />
          <div className="grid grid-cols-2 gap-3">
            <input
              type="date"
              className="border border-black/10 rounded-xl px-3 py-2 bg-white"
              value={form.deadline}
              onChange={(e) => setForm({ ...form, deadline: e.target.value })}
            />
            <input
              type="number"
              min="1"
              max="12"
              step="0.5"
              className="border border-black/10 rounded-xl px-3 py-2 bg-white"
              value={form.hours_per_day}
              onChange={(e) => setForm({ ...form, hours_per_day: Number(e.target.value) })}
            />
          </div>
          <button disabled={busy} className="bg-clay text-white rounded-xl px-4 py-2">
            {busy ? "Agents working..." : "Run the six agents"}
          </button>
        </form>
        <div className="mt-6 space-y-2">
          {goals.map((goal) => (
            <button
              key={goal.id}
              onClick={() => setOpen(goal)}
              className={`card w-full text-left p-4 ${open?.id === goal.id ? "ring-2 ring-clay" : ""}`}
            >
              <p className="font-medium">{goal.title}</p>
              <p className="text-sm text-ink/60">{goal.status}</p>
            </button>
          ))}
        </div>
      </div>
      {open && (
        <div className="card p-6">
          <div className="flex justify-between gap-3">
            <h3 className="font-serif text-2xl">{open.title}</h3>
            <button onClick={() => replan(open.id)} className="text-sm border border-black/15 rounded-lg px-3 py-1">
              Replan
            </button>
          </div>
          <p className="text-sm text-ink/60 mt-2">{open.description || "No extra notes."}</p>
          <div className="mt-5 space-y-3">
            {open.tasks.map((task) => (
              <div key={task.id} className="border-b border-black/5 pb-3">
                <p className="font-medium">{task.title}</p>
                <p className="text-sm text-ink/60">{task.details}</p>
                <p className="font-mono text-xs mt-1">
                  {task.priority} · {task.estimate_hours}h
                </p>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
