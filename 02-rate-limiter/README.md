# Project 2: Rate Limiter

## 📌 Problem Statement
Design a rate limiter middleware that restricts the number of requests a client can make to an API within a time window, protecting backend services from abuse and overload.

---

## ✅ Functional Requirements
- Limit requests per **user ID** and/or **IP address** per time window
- Return **HTTP 429 Too Many Requests** with a `Retry-After` header when limit is exceeded
- Support configurable rules: e.g. 100 req/min for free tier, 1000 req/min for paid tier
- Support multiple rule scopes: per-user, per-IP, per-endpoint
- Rules should be changeable without redeployment (config-driven)

## 🚫 Non-Functional Requirements
- **Latency**: add < 5ms overhead to each request
- **Distributed**: counters must be shared across multiple API server instances
- **Fault tolerant**: if the rate limiter store (Redis) goes down, fail open (allow traffic) rather than blocking everything
- **Accuracy**: allow up to ~0.1% error in counts (eventual consistency acceptable)
- **Scalability**: handle 50K requests/sec across all users

---

## 🔢 Estimations
- 10M active users
- Peak: 50,000 requests/sec
- Redis ops per request: 2 (read + increment) = 100K Redis ops/sec

---

## 🛠️ Recommended Tech Stack

| Layer | Technology | Why |
|-------|-----------|-----|
| **Middleware** | **Python** (FastAPI middleware) | Implement as a reusable middleware/decorator |
| **Counter Store** | **Redis** | Atomic `INCR` + `EXPIRE` — perfect for counters |
| **Config** | YAML / JSON file | Define rules without code changes |
| **Stretch goal** | **TypeScript** (Express middleware) | Re-implement as an Express.js middleware |
| **Stretch goal 2** | **C++** | Implement the algorithm (Token Bucket) in pure C++ as a library |

### What you'll learn:
- Redis atomic operations (`INCR`, `EXPIRE`, `Lua scripts`)
- Middleware/interceptor patterns in web frameworks
- Algorithm implementation: Token Bucket, Sliding Window
- Trade-off between accuracy and performance

---

## 🔗 Resources
- [DESIGN.md](./DESIGN.md)
- `diagrams/`
- `src/`
