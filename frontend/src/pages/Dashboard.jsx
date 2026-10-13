import { useEffect, useState } from "react";
import { api } from "../api";

export default function Dashboard() {
  const [overview, setOverview] = useState(null);
  const [goals, setGoals] = useState([]);

  useEffect(() => {
    api.overview().then(setOverview);
    api.goals().then(setGoals);
  }, []);

  return (
    <div>
      <p className="font-mono text-xs uppercase tracking-[0.2em] text-sage">Overview</p>
      <h2 className="font-serif text-4xl mt-2">A quieter way to run the week</h2>
      <p className="max-w-2xl mt-3 text-ink/70 leading-7">
        AgentOS turns a goal into tasks, a schedule, research notes, tool actions, an evaluation,
        and a replan if the first draft is too heavy.
      </p>
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 mt-8">
        {[
          ["Goals", overview?.goals],
          ["Tasks", overview?.tasks],
          ["Memory", overview?.memories],
          ["Last score", overview?.last_score ?? "—"],
        ].map(([label, value]) => (
          <div key={label} className="card p-5">
            <p className="text-sm text-ink/50">{label}</p>
            <p className="font-serif text-3xl mt-2">{value ?? "—"}</p>
          </div>
        ))}
      </div>
      <div className="card p-6 mt-6">
        <h3 className="font-serif text-2xl">Recent goals</h3>
        <div className="mt-4 space-y-3">
          {goals.map((goal) => (
            <div key={goal.id} className="flex justify-between gap-4 border-b border-black/5 pb-3">
              <div>
                <p className="font-medium">{goal.title}</p>
                <p className="text-sm text-ink/60">{goal.status} · {goal.tasks.length} tasks</p>
              </div>
              <p className="font-mono text-sm">{goal.run?.evaluation_score ?? "—"}/10</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
