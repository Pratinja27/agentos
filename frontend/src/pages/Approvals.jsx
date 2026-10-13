import { useEffect, useState } from "react";
import { api } from "../api";

export default function Approvals({ onChange }) {
  const [rows, setRows] = useState([]);

  async function load() {
    setRows(await api.approvals());
  }

  useEffect(() => {
    load();
  }, []);

  async function decide(id, decision) {
    await api.decide(id, decision);
    await load();
    onChange?.();
  }

  return (
    <div>
      <p className="font-mono text-xs uppercase tracking-[0.2em] text-sage">Human in the loop</p>
      <h2 className="font-serif text-4xl mt-2">Approve before tools act</h2>
      <div className="mt-8 space-y-3">
        {rows.map((row) => (
          <article key={row.id} className="card p-5 flex justify-between gap-4">
            <div>
              <p className="font-medium">{row.action}</p>
              <p className="text-sm text-ink/60 mt-1">{row.reason}</p>
              <p className="font-mono text-xs mt-2">{row.status}</p>
            </div>
            {row.status === "pending" && (
              <div className="flex gap-2">
                <button onClick={() => decide(row.id, "approve")} className="bg-sage text-white rounded-lg px-3 py-1">
                  Approve
                </button>
                <button onClick={() => decide(row.id, "reject")} className="border border-black/15 rounded-lg px-3 py-1">
                  Reject
                </button>
              </div>
            )}
          </article>
        ))}
        {!rows.length && <p>No tool actions waiting.</p>}
      </div>
    </div>
  );
}
