# Project 4: Task Queue / Job Scheduler

## 📌 Problem Statement
Design an async task queue system where producers submit background jobs (e.g. send email, resize image) and a pool of workers picks them up, executes them, and handles failures with retries.

---

## ✅ Functional Requirements
- **Submit a task**: producer sends a task with a type and JSON payload
- **Worker execution**: workers pull tasks and execute them
- **Task status tracking**: query whether a task is pending / running / done / failed
- **Retry on failure**: failed tasks are retried up to N times with backoff
- **Dead Letter Queue (DLQ)**: tasks that exceed max retries are moved to DLQ
- **Scheduled tasks**: submit a task to run at a specific future time (cron-like)
- **Priority queue**: high-priority tasks processed before low-priority ones

## 🚫 Non-Functional Requirements
- **At-least-once delivery**: a task must never be silently dropped
- **Idempotency**: workers should handle duplicate execution safely
- **Scalability**: add/remove workers dynamically without downtime
- **Fault tolerant**: worker crash must not lose the task (task re-queued)
- **Throughput**: process 1000 tasks/sec with 10 workers

---

## 🔢 Estimations
- 1M tasks/day → ~12 tasks/sec average, 100 tasks/sec peak
- Avg task duration: 500ms
- 10 parallel workers → 20 tasks/sec capacity

---

## 🛠️ Recommended Tech Stack

| Layer | Technology | Why |
|-------|-----------|-----|
| **Producer API** | **Python** (FastAPI) | Submit tasks via REST endpoint |
| **Worker** | **Python** | Workers are Python functions/classes |
| **Broker** | **Redis** (lists + sorted sets) | Use Redis as a queue — `LPUSH`/`BRPOP` for FIFO |
| **Task Status DB** | **PostgreSQL** | Practice SQL — store task state, retries, timestamps |
| **Stretch goal** | **TypeScript** | Re-implement producer as a TS/Node client |
| **Stretch goal 2** | **C++** | Implement a high-performance worker in C++ for CPU-heavy tasks |

### What you'll learn:
- Redis `LPUSH`, `BRPOP`, `ZADD` for queue mechanics
- PostgreSQL: `UPDATE` with status state machine, indexes on status column
- Worker pool patterns (threading / multiprocessing in Python)
- Retry logic with exponential backoff

---

## 🔗 Resources
- [DESIGN.md](./DESIGN.md)
- `diagrams/`
- `src/`
