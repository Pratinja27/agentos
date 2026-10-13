from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from .config import settings
from .database import Base, SessionLocal, engine, get_db
from .memory.store import add_memory
from .models import Approval, Goal, MemoryItem, ScheduleEvent
from .schemas import GoalCreate, GoalOut, MemoryCreate, MemoryOut, OverviewOut
from .seed import seed_if_empty
from .services import create_and_plan, overview, replan_goal

Base.metadata.create_all(bind=engine)
app = FastAPI(title="AgentOS API", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[origin.strip() for origin in settings.cors_origins.split(",") if origin.strip()],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup() -> None:
    db = SessionLocal()
    try:
        seed_if_empty(db)
    finally:
        db.close()


@app.get("/api/health")
def health():
    return {"ok": True, "name": "AgentOS"}


@app.get("/api/overview", response_model=OverviewOut)
def get_overview(db: Session = Depends(get_db)):
    return overview(db)


@app.get("/api/goals", response_model=list[GoalOut])
def list_goals(db: Session = Depends(get_db)):
    return db.query(Goal).order_by(Goal.id.desc()).all()


@app.post("/api/goals", response_model=GoalOut)
def create_goal(payload: GoalCreate, db: Session = Depends(get_db)):
    return create_and_plan(db, payload)


@app.get("/api/goals/{goal_id}", response_model=GoalOut)
def get_goal(goal_id: int, db: Session = Depends(get_db)):
    goal = db.query(Goal).filter(Goal.id == goal_id).first()
    if not goal:
        raise HTTPException(404, "Goal not found")
    return goal


@app.post("/api/goals/{goal_id}/replan", response_model=GoalOut)
def replan(goal_id: int, db: Session = Depends(get_db)):
    goal = db.query(Goal).filter(Goal.id == goal_id).first()
    if not goal:
        raise HTTPException(404, "Goal not found")
    return replan_goal(db, goal)


@app.get("/api/schedule")
def schedule(db: Session = Depends(get_db)):
    events = db.query(ScheduleEvent).order_by(ScheduleEvent.day, ScheduleEvent.start_time).all()
    return [
        {
            "id": event.id,
            "goal_id": event.goal_id,
            "task_title": event.task_title,
            "day": event.day,
            "start_time": event.start_time,
            "end_time": event.end_time,
            "kind": event.kind,
        }
        for event in events
    ]


@app.get("/api/approvals")
def approvals(db: Session = Depends(get_db)):
    rows = db.query(Approval).order_by(Approval.id.desc()).all()
    return rows


@app.post("/api/approvals/{approval_id}/{decision}")
def decide(approval_id: int, decision: str, db: Session = Depends(get_db)):
    if decision not in {"approve", "reject"}:
        raise HTTPException(400, "Use approve or reject")
    row = db.query(Approval).filter(Approval.id == approval_id).first()
    if not row:
        raise HTTPException(404, "Approval not found")
    row.status = "approved" if decision == "approve" else "rejected"
    goal = db.query(Goal).filter(Goal.id == row.goal_id).first()
    if goal and not any(item.status == "pending" for item in goal.approvals):
        goal.status = "active"
    db.commit()
    return {"id": row.id, "status": row.status}


@app.get("/api/memory", response_model=list[MemoryOut])
def list_memory(db: Session = Depends(get_db)):
    return db.query(MemoryItem).order_by(MemoryItem.id.desc()).all()


@app.post("/api/memory", response_model=MemoryOut)
def create_memory(payload: MemoryCreate, db: Session = Depends(get_db)):
    return add_memory(db, payload.kind, payload.title, payload.content)
