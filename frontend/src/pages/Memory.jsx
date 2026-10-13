import { useEffect, useState } from "react";
import { api } from "../api";

export default function Memory({ onChange }) {
  const [items, setItems] = useState([]);
  const [form, setForm] = useState({ kind: "preference", title: "", content: "" });

  async function load() {
    setItems(await api.memory());
  }

  useEffect(() => {
    load();
  }, []);

  async function submit(event) {
    event.preventDefault();
    await api.addMemory(form);
    setForm({ kind: "preference", title: "", content: "" });
    await load();
    onChange?.();
  }

  return (
    <div className="grid lg:grid-cols-2 gap-6">
      <div>
        <p className="font-mono text-xs uppercase tracking-[0.2em] text-sage">Persistent memory</p>
        <h2 className="font-serif text-4xl mt-2">What AgentOS remembers</h2>
        <form className="card p-6 mt-6 space-y-3" onSubmit={submit}>
          <select
            className="w-full border border-black/10 rounded-xl px-3 py-2 bg-white"
            value={form.kind}
            onChange={(e) => setForm({ ...form, kind: e.target.value })}
          >
            <option value="preference">preference</option>
            <option value="activity">activity</option>
          </select>
          <input
            className="w-full border border-black/10 rounded-xl px-3 py-2 bg-white"
            placeholder="Morning deep work"
            value={form.title}
            onChange={(e) => setForm({ ...form, title: e.target.value })}
            required
          />
          <textarea
            className="w-full border border-black/10 rounded-xl px-3 py-2 bg-white min-h-24"
            placeholder="Store a preference the next plan should respect"
            value={form.content}
            onChange={(e) => setForm({ ...form, content: e.target.value })}
            required
          />
          <button className="bg-moss text-paper rounded-xl px-4 py-2">Save to memory</button>
        </form>
      </div>
      <div className="space-y-3">
        {items.map((item) => (
          <article key={item.id} className="card p-5">
            <p className="font-mono text-xs uppercase text-sage">{item.kind}</p>
            <h3 className="font-serif text-xl mt-1">{item.title}</h3>
            <p className="text-sm text-ink/70 mt-2">{item.content}</p>
          </article>
        ))}
      </div>
    </div>
  );
}
