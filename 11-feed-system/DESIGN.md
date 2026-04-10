# Design: Feed System

## 🏗️ High-Level Architecture

### Fan-out on Write
```
User posts → Write to followers' feed caches immediately
           → Fast reads, slow writes
```

### Fan-out on Read
```
User requests feed → Pull posts from all followed users at read time
                   → Slow reads, fast writes
```

---

## 🔑 Key Components
- **Post Service**: Stores posts in DB
- **Follow Graph**: User → [following list]
- **Feed Cache**: Redis list per user (pre-computed timeline)
- **Hybrid approach**: Fan-out on write for normal users, on read for celebrities

---

## ⚖️ Design Decisions & Tradeoffs

| Decision | Option A | Option B | Chosen | Why |
|----------|----------|----------|--------|-----|
| Fan-out | On write | On read | Hybrid | |
| Feed storage | Redis list | DB query | | |
| Ranking | Chronological | Algorithmic | | |

---

## 🤔 Open Questions
- [ ] How to handle celebrities with 10M+ followers?
- [ ] How to rank/filter feed posts?
- [ ] How far back should the feed go?
