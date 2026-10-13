from datetime import datetime

from pydantic import BaseModel, Field


class GoalCreate(BaseModel):
    title: str = Field(min_length=3, max_length=240)
    description: str = ""
    deadline: str = ""
    hours_per_day: float = 4


class TaskOut(BaseModel):
    id: int
    title: str
    details: str
    priority: str
    estimate_hours: float
    status: str

    class Config:
        from_attributes = True


class EventOut(BaseModel):
    id: int
    task_title: str
    day: str
    start_time: str
    end_time: str
    kind: str

    class Config:
        from_attributes = True


class TraceOut(BaseModel):
    id: int
    agent: str
    summary: str
    detail: str
    created_at: datetime

    class Config:
        from_attributes = True


class ApprovalOut(BaseModel):
    id: int
    goal_id: int
    action: str
    reason: str
    status: str

    class Config:
        from_attributes = True


class AgentRunOut(BaseModel):
    id: int
    mode: str
    evaluation_score: float
    evaluation_notes: str
    replanned: bool
    research_notes: str
    traces: list[TraceOut] = []

    class Config:
        from_attributes = True


class GoalOut(BaseModel):
    id: int
    title: str
    description: str
    deadline: str
    hours_per_day: float
    status: str
    created_at: datetime
    tasks: list[TaskOut] = []
    events: list[EventOut] = []
    approvals: list[ApprovalOut] = []
    run: AgentRunOut | None = None

    class Config:
        from_attributes = True


class MemoryOut(BaseModel):
    id: int
    kind: str
    title: str
    content: str
    created_at: datetime

    class Config:
        from_attributes = True


class MemoryCreate(BaseModel):
    kind: str = "preference"
    title: str
    content: str


class OverviewOut(BaseModel):
    goals: int
    tasks: int
    pending_approvals: int
    memories: int
    last_score: float | None = None
    llm_mode: str
