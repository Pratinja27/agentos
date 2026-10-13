# AgentOS

AgentOS is an agentic AI life and task management system. Conventional to-do apps ask the user to break goals down, pick priorities, build a calendar, and redo the plan when life changes. AgentOS does that loop with six cooperating agents and keeps a memory of what the user prefers.

This repository is the working demonstration of the research abstract *AgentOS – An Agentic AI Life and Task Management System*.

## Why it exists

Task tools stay manual. Research systems usually solve one slice of the problem: planning (LLM+P), memory and reflection (Generative Agents, Reflexion), tool use (ReAct), multi-agent talk (AutoGen), or evaluation (AgentBench). AgentOS puts those pieces into one personal productivity architecture.

## What the system does

1. A user states a goal and constraints (deadline, hours per day, work / study / health).
2. **Planner** turns the goal into tasks.
3. **Scheduler** places those tasks on a week.
4. **Researcher** adds short notes and method hints.
5. **Executor** prepares tool actions but does not fire them blindly.
6. **Evaluator** scores load, recovery, and fit.
7. **Replanner** rewrites the week if the first draft is too heavy.
8. A memory layer stores preferences and past outcomes so the next plan is more personal.
9. Human approval sits in front of calendar writes and messages.

## Architecture

```
React + Tailwind UI
        |
     FastAPI
        |
 LangGraph-style agent graph
        |
 PostgreSQL / SQLite     ChromaDB memory     Gemini (optional)
```

- Frontend: React and Tailwind CSS
- Backend: FastAPI and Python
- Agent graph: Planner → Scheduler → Researcher → Executor → Evaluator → Replanner
- Structured data: PostgreSQL in Docker, SQLite for a local demo
- Semantic memory: ChromaDB, with a SQL fallback
- Reasoning: Google Gemini when `GEMINI_API_KEY` is set; otherwise a built-in demo planner so the project still runs

## Research mapping

| Paper / idea | AgentOS part |
| --- | --- |
| LLM+P | Planner and Scheduler |
| Generative Agents | Persistent memory |
| Reflexion | Evaluator and Replanner |
| ReAct | Researcher and Executor |
| AutoGen | Multi-agent handoff and human approval |
| AgentBench | Evaluation score on each run |

## Project contents

- Working web application for goals, schedule, agent traces, memory, and approvals
- Docker Compose setup for PostgreSQL, API, and UI
