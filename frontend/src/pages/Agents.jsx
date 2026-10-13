import { useEffect, useState } from "react";
import { api } from "../api";

const order = ["planner", "scheduler", "researcher", "executor", "evaluator", "replanner"];

export default function Agents() {
  const [goal, setGoal] = useState(null);

  useEffect(() => {
    api.goals().then((rows) => setGoal(rows[0] || null));
  }, []);

  const traces = goal?.run?.traces || [];

  return (
    <div>
      <p className="font-mono text-xs uppercase tracking-[0.2em] text-sage">LangGraph-style pipeline</p>
      <h2 className="font-serif text-4xl mt-2">Six agents, one loop</h2>
      <p className="mt-3 text-ink/70 max-w-2xl">
        Planner → Scheduler → Researcher → Executor → Evaluator → Replanner. This is the same
        research mapping used in the 5-week and 15-week reports.
      </p>
      <div className="flex flex-wrap gap-2 mt-6">
        {order.map((name) => (
          <span key={name} className="px-3 py-1 rounded-full bg-moss text-paper text-sm capitalize">
            {name}
          </span>
        ))}
      </div>
      <div className="card p-6 mt-6 space-y-4">
        <p className="text-sm text-ink/60">
          Latest run for: {goal?.title || "no goal yet"} · score {goal?.run?.evaluation_score ?? "—"} ·{" "}
          {goal?.run?.replanned ? "replanned" : "first draft kept"}
        </p>
        {traces.map((trace) => (
          <div key={trace.id} className="border-l-2 border-clay pl-4">
            <p className="font-mono text-xs uppercase tracking-wider text-clay">{trace.agent}</p>
            <p className="font-medium mt-1">{trace.summary}</p>
            <p className="text-sm text-ink/65 mt-1">{trace.detail}</p>
          </div>
        ))}
      </div>
    </div>
  );
}
