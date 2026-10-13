from __future__ import annotations

from datetime import date, timedelta

from .llm import complete_json, llm_mode


AGENTS = ["planner", "scheduler", "researcher", "executor", "evaluator", "replanner"]


def _days(n: int = 5) -> list[str]:
    start = date.today()
    return [(start + timedelta(days=i)).isoformat() for i in range(n)]


def _looks_like(text: str, words: tuple[str, ...]) -> bool:
    blob = text.lower()
    return any(word in blob for word in words)


def demo_plan(title: str, description: str, hours: float) -> dict:
    text = f"{title} {description}"
    tasks = []
    if _looks_like(text, ("exam", "study", "semester", "assignment", "research")):
        tasks.extend(
            [
                ("Map syllabus and weak topics", "List units, marks weight, and weak chapters.", "high", 2),
                ("Daily concept revision", "Short revision blocks with notes and flashcards.", "high", 1.5),
                ("Past-paper practice", "Timed questions and error log.", "high", 2),
            ]
        )
    if _looks_like(text, ("gym", "health", "fitness", "workout", "sleep")):
        tasks.extend(
            [
                ("Strength or cardio session", "Keep a fixed 45-minute health slot.", "medium", 1),
                ("Sleep and recovery window", "Protect a no-screen wind-down hour.", "medium", 1),
            ]
        )
    if _looks_like(text, ("job", "work", "intern", "shift", "office")):
        tasks.extend(
            [
                ("Protected work block", "Deep work for the job or internship.", "high", 3),
                ("Weekly review with manager notes", "Capture blockers and next actions.", "medium", 0.5),
            ]
        )
    if not tasks:
        tasks = [
            ("Clarify the outcome", "Write a one-page definition of done.", "high", 1),
            ("Break work into daily slices", "Create small completable units.", "high", 1.5),
            ("Review and adjust", "Check progress and move leftover work.", "medium", 0.5),
        ]
    tasks.append(("Weekly reflection", "Store what worked in memory for the next plan.", "low", 0.5))
    return {
        "tasks": [
            {
                "title": title_,
                "details": details,
                "priority": priority,
                "estimate_hours": hours_,
            }
            for title_, details, priority, hours_ in tasks
        ]
    }


def demo_schedule(tasks: list[dict], hours_per_day: float) -> dict:
    days = _days()
    events = []
    start_hour = 9
    used = 0.0
    day_index = 0
    for task in tasks:
        remaining = float(task["estimate_hours"])
        while remaining > 0 and day_index < len(days):
            room = max(1.0, hours_per_day - used)
            chunk = min(remaining, room, 2.0)
            end = start_hour + chunk
            kind = "health" if _looks_like(task["title"], ("gym", "sleep", "health")) else "focus"
            events.append(
                {
                    "task_title": task["title"],
                    "day": days[day_index],
                    "start_time": f"{int(start_hour):02d}:00",
                    "end_time": f"{int(end):02d}:{int((end % 1) * 60):02d}",
                    "kind": kind,
                }
            )
            remaining -= chunk
            used += chunk
            start_hour = end + 0.5
            if used >= hours_per_day:
                day_index += 1
                used = 0
                start_hour = 9
    return {"events": events}


def demo_research(title: str) -> dict:
    return {
        "notes": (
            f"Researcher looked up planning patterns for '{title}'. "
            "Useful ideas: time-box deep work, keep one recovery slot, "
            "and review errors the same day they appear. "
            "Mapped from ReAct (reason then act) and LLM+P (plan then execute)."
        )
    }


def demo_actions(title: str) -> dict:
    return {
        "approvals": [
            {
                "action": "Add the generated study and work blocks to the calendar",
                "reason": "Calendar writes change the user's real week, so AgentOS waits for approval.",
            },
            {
                "action": f"Send a daily reminder for: {title}",
                "reason": "External messages should not be sent without human confirmation.",
            },
        ]
    }


def demo_evaluate(tasks: list[dict], events: list[dict], hours_per_day: float) -> dict:
    load = sum(float(task["estimate_hours"]) for task in tasks)
    days = max(1, len({event["day"] for event in events}) or 1)
    daily = load / days
    issues = []
    if daily > hours_per_day:
        issues.append("The plan is heavier than the daily hour budget.")
    if not any(_looks_like(task["title"], ("sleep", "health", "gym", "review", "reflection")) for task in tasks):
        issues.append("Recovery or review is missing.")
    score = 8.6 if not issues else 6.4
    return {
        "score": score,
        "notes": " ".join(issues) if issues else "The plan fits the hour budget and keeps a review loop.",
        "needs_replan": bool(issues),
    }


def demo_replan(tasks: list[dict], hours_per_day: float) -> dict:
    reduced = []
    for task in tasks:
        hours = min(float(task["estimate_hours"]), max(0.5, hours_per_day / 2))
        reduced.append({**task, "estimate_hours": hours})
    return {"tasks": reduced, "reason": "Replanner cut overload and kept high-priority work first."}


def run_pipeline(goal: dict, memory_hints: list[str]) -> dict:
    context = "\n".join(memory_hints) or "No prior memory."
    hours = float(goal.get("hours_per_day") or 4)
    plan = complete_json(
        (
            "You are the Planner agent in AgentOS. Break the user goal into 4-7 tasks. "
            f"Goal: {goal['title']}. Details: {goal.get('description','')}. "
            f"Deadline: {goal.get('deadline','')}. Hours/day: {hours}. Memory: {context}. "
            'JSON shape: {"tasks":[{"title":"","details":"","priority":"high|medium|low","estimate_hours":1}]}'
        ),
        demo_plan(goal["title"], goal.get("description", ""), hours),
    )
    tasks = plan.get("tasks") or demo_plan(goal["title"], goal.get("description", ""), hours)["tasks"]

    schedule = complete_json(
        (
            "You are the Scheduler agent. Place tasks on the next 5 days without exceeding daily hours. "
            f"Hours/day: {hours}. Tasks: {tasks}. "
            'JSON shape: {"events":[{"task_title":"","day":"YYYY-MM-DD","start_time":"HH:MM","end_time":"HH:MM","kind":"focus|health"}]}'
        ),
        demo_schedule(tasks, hours),
    )
    events = schedule.get("events") or demo_schedule(tasks, hours)["events"]

    research = complete_json(
        f"You are the Researcher agent. Give short useful notes for this goal: {goal['title']}. JSON: {{'notes':''}}",
        demo_research(goal["title"]),
    )
    actions = demo_actions(goal["title"])
    evaluation = demo_evaluate(tasks, events, hours)
    replanned = False
    replan_reason = ""

    if evaluation["needs_replan"]:
        revised = demo_replan(tasks, hours)
        tasks = revised["tasks"]
        events = demo_schedule(tasks, hours)["events"]
        evaluation = demo_evaluate(tasks, events, hours)
        evaluation["notes"] = revised["reason"] + " " + evaluation["notes"]
        replanned = True
        replan_reason = revised["reason"]

    traces = [
        ("planner", "Broke the goal into executable tasks.", f"{len(tasks)} tasks created."),
        ("scheduler", "Placed work on a 5-day calendar.", f"{len(events)} blocks scheduled."),
        ("researcher", "Collected planning notes and related methods.", research.get("notes", "")),
        ("executor", "Prepared tool actions that need human approval.", f"{len(actions['approvals'])} actions queued."),
        ("evaluator", f"Scored the plan {evaluation['score']}/10.", evaluation["notes"]),
    ]
    if replanned:
        traces.append(("replanner", "Revised the plan after evaluation.", replan_reason))
    else:
        traces.append(("replanner", "No rewrite needed.", "Evaluator accepted the first plan."))

    return {
        "mode": llm_mode(),
        "tasks": tasks,
        "events": events,
        "research_notes": research.get("notes", ""),
        "approvals": actions["approvals"],
        "score": evaluation["score"],
        "evaluation_notes": evaluation["notes"],
        "replanned": replanned,
        "traces": traces,
    }
