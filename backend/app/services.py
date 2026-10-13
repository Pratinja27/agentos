from sqlalchemy.orm import Session

from .agents.llm import llm_mode
from .agents.pipeline import run_pipeline
from .memory.store import add_memory, search_memory
from .models import AgentRun, AgentTrace, Approval, Goal, MemoryItem, ScheduleEvent, Task


def persist_pipeline(db: Session, goal: Goal, result: dict) -> Goal:
    for task in result["tasks"]:
        db.add(
            Task(
                goal_id=goal.id,
                title=task["title"],
                details=task.get("details", ""),
                priority=task.get("priority", "medium"),
                estimate_hours=float(task.get("estimate_hours") or 1),
            )
        )
    for event in result["events"]:
        db.add(
            ScheduleEvent(
                goal_id=goal.id,
                task_title=event["task_title"],
                day=event["day"],
                start_time=event["start_time"],
                end_time=event["end_time"],
                kind=event.get("kind", "focus"),
            )
        )
    run = AgentRun(
        goal_id=goal.id,
        mode=result["mode"],
        evaluation_score=result["score"],
        evaluation_notes=result["evaluation_notes"],
        replanned=result["replanned"],
        research_notes=result["research_notes"],
    )
    db.add(run)
    db.flush()
    for agent, summary, detail in result["traces"]:
        db.add(AgentTrace(run_id=run.id, agent=agent, summary=summary, detail=detail))
    for item in result["approvals"]:
        db.add(Approval(goal_id=goal.id, action=item["action"], reason=item["reason"]))
    goal.status = "needs_approval" if result["approvals"] else "scheduled"
    add_memory(
        db,
        "activity",
        f"Plan for {goal.title}",
        f"Score {result['score']}. {result['evaluation_notes']}",
    )
    db.commit()
    db.refresh(goal)
    return goal


def create_and_plan(db: Session, payload) -> Goal:
    goal = Goal(
        title=payload.title,
        description=payload.description,
        deadline=payload.deadline,
        hours_per_day=payload.hours_per_day,
        status="planning",
    )
    db.add(goal)
    db.commit()
    db.refresh(goal)
    hints = [f"{item.title}: {item.content}" for item in search_memory(db, payload.title)]
    result = run_pipeline(
        {
            "title": goal.title,
            "description": goal.description,
            "deadline": goal.deadline,
            "hours_per_day": goal.hours_per_day,
        },
        hints,
    )
    return persist_pipeline(db, goal, result)


def replan_goal(db: Session, goal: Goal) -> Goal:
    db.query(Task).filter(Task.goal_id == goal.id).delete()
    db.query(ScheduleEvent).filter(ScheduleEvent.goal_id == goal.id).delete()
    db.query(Approval).filter(Approval.goal_id == goal.id).delete()
    if goal.run:
        db.delete(goal.run)
    db.commit()
    hints = [f"{item.title}: {item.content}" for item in search_memory(db, goal.title)]
    result = run_pipeline(
        {
            "title": goal.title,
            "description": goal.description + " Replan with a lighter load and clearer recovery time.",
            "deadline": goal.deadline,
            "hours_per_day": max(2, goal.hours_per_day - 0.5),
        },
        hints,
    )
    result["replanned"] = True
    return persist_pipeline(db, goal, result)


def overview(db: Session) -> dict:
    last = db.query(AgentRun).order_by(AgentRun.id.desc()).first()
    return {
        "goals": db.query(Goal).count(),
        "tasks": db.query(Task).count(),
        "pending_approvals": db.query(Approval).filter(Approval.status == "pending").count(),
        "memories": db.query(MemoryItem).count(),
        "last_score": last.evaluation_score if last else None,
        "llm_mode": llm_mode(),
    }
