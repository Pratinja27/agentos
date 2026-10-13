from datetime import datetime

from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .database import Base


class Goal(Base):
    __tablename__ = "goals"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(240))
    description: Mapped[str] = mapped_column(Text, default="")
    deadline: Mapped[str] = mapped_column(String(40), default="")
    hours_per_day: Mapped[float] = mapped_column(Float, default=4)
    status: Mapped[str] = mapped_column(String(40), default="planned")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    tasks: Mapped[list["Task"]] = relationship(back_populates="goal", cascade="all, delete-orphan")
    events: Mapped[list["ScheduleEvent"]] = relationship(back_populates="goal", cascade="all, delete-orphan")
    run: Mapped["AgentRun"] = relationship(back_populates="goal", uselist=False, cascade="all, delete-orphan")
    approvals: Mapped[list["Approval"]] = relationship(back_populates="goal", cascade="all, delete-orphan")


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    goal_id: Mapped[int] = mapped_column(ForeignKey("goals.id"))
    title: Mapped[str] = mapped_column(String(240))
    details: Mapped[str] = mapped_column(Text, default="")
    priority: Mapped[str] = mapped_column(String(20), default="medium")
    estimate_hours: Mapped[float] = mapped_column(Float, default=1)
    status: Mapped[str] = mapped_column(String(40), default="ready")
    goal: Mapped[Goal] = relationship(back_populates="tasks")


class ScheduleEvent(Base):
    __tablename__ = "schedule_events"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    goal_id: Mapped[int] = mapped_column(ForeignKey("goals.id"))
    task_title: Mapped[str] = mapped_column(String(240))
    day: Mapped[str] = mapped_column(String(40))
    start_time: Mapped[str] = mapped_column(String(20))
    end_time: Mapped[str] = mapped_column(String(20))
    kind: Mapped[str] = mapped_column(String(40), default="work")
    goal: Mapped[Goal] = relationship(back_populates="events")


class AgentRun(Base):
    __tablename__ = "agent_runs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    goal_id: Mapped[int] = mapped_column(ForeignKey("goals.id"), unique=True)
    mode: Mapped[str] = mapped_column(String(40), default="demo")
    evaluation_score: Mapped[float] = mapped_column(Float, default=0)
    evaluation_notes: Mapped[str] = mapped_column(Text, default="")
    replanned: Mapped[bool] = mapped_column(Boolean, default=False)
    research_notes: Mapped[str] = mapped_column(Text, default="")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    goal: Mapped[Goal] = relationship(back_populates="run")
    traces: Mapped[list["AgentTrace"]] = relationship(back_populates="run", cascade="all, delete-orphan")


class AgentTrace(Base):
    __tablename__ = "agent_traces"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    run_id: Mapped[int] = mapped_column(ForeignKey("agent_runs.id"))
    agent: Mapped[str] = mapped_column(String(40))
    summary: Mapped[str] = mapped_column(Text, default="")
    detail: Mapped[str] = mapped_column(Text, default="")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    run: Mapped[AgentRun] = relationship(back_populates="traces")


class Approval(Base):
    __tablename__ = "approvals"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    goal_id: Mapped[int] = mapped_column(ForeignKey("goals.id"))
    action: Mapped[str] = mapped_column(String(240))
    reason: Mapped[str] = mapped_column(Text, default="")
    status: Mapped[str] = mapped_column(String(20), default="pending")
    goal: Mapped[Goal] = relationship(back_populates="approvals")


class MemoryItem(Base):
    __tablename__ = "memory_items"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    kind: Mapped[str] = mapped_column(String(40))
    title: Mapped[str] = mapped_column(String(240))
    content: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
