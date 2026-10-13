import { useEffect, useState } from "react";
import { api } from "../api";

export default function Schedule() {
  const [events, setEvents] = useState([]);

  useEffect(() => {
    api.schedule().then(setEvents);
  }, []);

  const days = [...new Set(events.map((event) => event.day))];

  return (
    <div>
      <p className="font-mono text-xs uppercase tracking-[0.2em] text-sage">Scheduler</p>
      <h2 className="font-serif text-4xl mt-2">The week the agents proposed</h2>
      <div className="grid md:grid-cols-2 xl:grid-cols-3 gap-4 mt-8">
        {days.map((day) => (
          <section key={day} className="card p-5">
            <h3 className="font-serif text-xl">{day}</h3>
            <div className="mt-4 space-y-3">
              {events
                .filter((event) => event.day === day)
                .map((event) => (
                  <div key={event.id} className="bg-paper rounded-xl px-3 py-2">
                    <p className="font-mono text-xs text-sage">
                      {event.start_time}–{event.end_time}
                    </p>
                    <p className="text-sm mt-1">{event.task_title}</p>
                    <p className="text-xs text-ink/50">{event.kind}</p>
                  </div>
                ))}
            </div>
          </section>
        ))}
        {!days.length && <p>No schedule yet. Create a goal first.</p>}
      </div>
    </div>
  );
}
