from sqlalchemy.orm import Session

from .memory.store import add_memory
from .models import Approval, Goal, MemoryItem


def seed_if_empty(db: Session) -> None:
    if db.query(MemoryItem).count() == 0:
        add_memory(db, "preference", "Deep work mornings", "User prefers focused study before 12:00.")
        add_memory(db, "preference", "Protect gym time", "Do not overwrite evening workout slots.")
        add_memory(db, "preference", "Ask before external actions", "Calendar writes and messages need approval.")
        add_memory(db, "activity", "Earlier exam week", "A 4-hour daily cap worked better than 7-hour cram days.")

    if db.query(Goal).count() == 0:
        from .schemas import GoalCreate
        from .services import create_and_plan

        create_and_plan(
            db,
            GoalCreate(
                title="Prepare for semester exams while keeping gym and part-time work",
                description="Need a balanced week: exam revision, 45-minute gym, and job shifts.",
                deadline="2026-10-15",
                hours_per_day=5,
            ),
        )
        pending = db.query(Approval).filter(Approval.status == "pending").first()
        if pending:
            pending.status = "approved"
            db.commit()
