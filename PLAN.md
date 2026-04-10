# System Design Mini Projects — Learning Plan

## 🎯 Goal
Build hands-on experience with system design concepts through progressively complex mini projects.

---

## 📚 Learning Path Overview

### Phase 1 — Foundations (Weeks 1–4)
> Focus: Core building blocks of any system

| # | Project | Key Concepts |
|---|---------|-------------|
| 1 | **URL Shortener** (like bit.ly) | Hashing, Databases, REST API, Caching |
| 2 | **Rate Limiter** | Algorithms (Token Bucket, Sliding Window), Redis |
| 3 | **Key-Value Store** (like Redis lite) | Storage engines, In-memory design |

---

### Phase 2 — Scalability (Weeks 5–9)
> Focus: How systems handle growth

| # | Project | Key Concepts |
|---|---------|-------------|
| 4 | **Task Queue / Job Scheduler** | Message queues, Workers, Async processing |
| 5 | **Notification System** | Fan-out, Pub/Sub, Push vs Pull |
| 6 | **Leaderboard System** | Sorted sets, Real-time updates, Redis |

---

### Phase 3 — Distributed Systems (Weeks 10–15)
> Focus: Multi-node thinking

| # | Project | Key Concepts |
|---|---------|-------------|
| 7 | **Distributed Cache** (like Memcached) | Consistent hashing, Eviction policies |
| 8 | **Search Autocomplete** | Trie, Indexing, Typeahead |
| 9 | **Simple Distributed File System** | Replication, Fault tolerance, Chunking |

---

### Phase 4 — Real-World Systems (Weeks 16–22)
> Focus: Simulate production-like systems

| # | Project | Key Concepts |
|---|---------|-------------|
| 10 | **Chat System** (like WhatsApp basic) | WebSockets, Message delivery, Storage |
| 11 | **Feed System** (like Twitter timeline) | Fan-out on write/read, Caching strategy |
| 12 | **Video Upload & Streaming** (like YouTube lite) | CDN, Chunked upload, Encoding pipeline |

---

## 🧱 Core Concepts Covered Across All Projects

- [ ] Load Balancing
- [ ] Caching (L1, L2, CDN)
- [ ] Database design (SQL vs NoSQL)
- [ ] CAP Theorem
- [ ] Horizontal vs Vertical scaling
- [ ] Message Queues
- [ ] API Design (REST / gRPC)
- [ ] Monitoring & Observability
- [ ] Rate Limiting & Security basics

---

## 📁 Directory Structure

```
system_design/
├── PLAN.md                          ← You are here
├── 01-url-shortener/
│   ├── README.md
│   ├── DESIGN.md
│   ├── src/
│   └── diagrams/
├── 02-rate-limiter/
│   ├── README.md
│   ├── DESIGN.md
│   ├── src/
│   └── diagrams/
├── 03-key-value-store/
│   ├── README.md
│   ├── DESIGN.md
│   ├── src/
│   └── diagrams/
├── 04-task-queue/
│   ├── README.md
│   ├── DESIGN.md
│   ├── src/
│   └── diagrams/
├── 05-notification-system/
│   ├── README.md
│   ├── DESIGN.md
│   ├── src/
│   └── diagrams/
├── 06-leaderboard/
│   ├── README.md
│   ├── DESIGN.md
│   ├── src/
│   └── diagrams/
├── 07-distributed-cache/
│   ├── README.md
│   ├── DESIGN.md
│   ├── src/
│   └── diagrams/
├── 08-search-autocomplete/
│   ├── README.md
│   ├── DESIGN.md
│   ├── src/
│   └── diagrams/
├── 09-distributed-file-system/
│   ├── README.md
│   ├── DESIGN.md
│   ├── src/
│   └── diagrams/
├── 10-chat-system/
│   ├── README.md
│   ├── DESIGN.md
│   ├── src/
│   └── diagrams/
├── 11-feed-system/
│   ├── README.md
│   ├── DESIGN.md
│   ├── src/
│   └── diagrams/
└── 12-video-streaming/
    ├── README.md
    ├── DESIGN.md
    ├── src/
    └── diagrams/
```

---

## 🛠️ Tools & Stack Suggestions
- **Diagramming**: draw.io, Excalidraw
- **Implementation**: Python / Go (your choice)
- **Storage**: PostgreSQL, Redis, SQLite
- **Queue**: RabbitMQ or simple in-memory queue
- **Docs**: Markdown in this repo

---

## ✅ Definition of Done (per project)
- [ ] Requirements defined (functional + non-functional)
- [ ] High-level architecture diagram created
- [ ] Key design decisions documented with tradeoffs
- [ ] At least one deep-dive on the hardest component
- [ ] (Optional) Working prototype

---

## 🚀 Start Here → [Project 1: URL Shortener](./01-url-shortener/README.md)
