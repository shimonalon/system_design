# Design: Task Queue / Job Scheduler

## 🏗️ High-Level Architecture
```
Producer → Message Broker (Queue) → Workers (Consumers)
                                  → Dead Letter Queue (failed jobs)
               ↕
           DB (job status tracking)
```

---

## 🔑 Key Components
- **Producer**: Submits jobs to queue
- **Broker**: RabbitMQ / Redis / SQS
- **Worker**: Pulls and executes jobs
- **DLQ**: Dead Letter Queue for failed jobs

---

## ⚖️ Design Decisions & Tradeoffs

| Decision | Option A | Option B | Chosen | Why |
|----------|----------|----------|--------|-----|
| Broker | RabbitMQ | Redis Queue | | |
| Delivery | At-least-once | Exactly-once | | |
| Priority | FIFO | Priority Queue | | |

---

## 🤔 Open Questions
- [ ] How to handle duplicate job execution?
- [ ] How to scale workers dynamically?
- [ ] How long to retain completed job history?
