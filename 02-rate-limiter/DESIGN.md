# Design: Rate Limiter

## 🏗️ High-Level Architecture
```
Client → Rate Limiter Middleware → API Server
               ↕
            Redis (counters)
```

---

## 🔑 Key Algorithms

### Options:
- [ ] **Token Bucket** — Smooth burst handling
- [ ] **Leaky Bucket** — Strict output rate
- [ ] **Fixed Window Counter** — Simple, but boundary issues
- [ ] **Sliding Window Log** — Accurate, memory heavy
- [ ] **Sliding Window Counter** — Balanced approach

### Chosen Algorithm:
> (Fill in your choice and reasoning)

---

## 🗃️ Redis Data Structure
```
KEY:   rate_limit:{user_id}:{window}
VALUE: request count
TTL:   window size in seconds
```

---

## ⚖️ Design Decisions & Tradeoffs

| Decision | Option A | Option B | Chosen | Why |
|----------|----------|----------|--------|-----|
| Algorithm | Token Bucket | Sliding Window | | |
| Storage | Redis | In-memory | | |
| Scope | Per user | Per IP | | |

---

## 🤔 Open Questions
- [ ] How to handle Redis failure? (fail open vs fail closed)
- [ ] How to sync counters across distributed nodes?
- [ ] Where to place the limiter? (client / gateway / server)
