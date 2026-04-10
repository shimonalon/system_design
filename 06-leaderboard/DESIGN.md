# Design: Leaderboard System

## 🏗️ High-Level Architecture
```
Client → API Server → Redis Sorted Set (ZSET)
                    → DB (persistent scores)
```

---

## 🔑 Key Components
- **Redis ZSET**: `ZADD`, `ZRANK`, `ZRANGE` for O(log N) ops
- **Database**: Persistent storage for scores
- **Cache**: Redis as primary leaderboard store

---

## Redis Commands
```
ZADD  leaderboard {score} {user_id}   # add/update score
ZREVRANGE leaderboard 0 9 WITHSCORES  # top 10
ZREVRANK  leaderboard {user_id}        # player rank
```

---

## ⚖️ Design Decisions & Tradeoffs

| Decision | Option A | Option B | Chosen | Why |
|----------|----------|----------|--------|-----|
| Storage | Redis ZSET | SQL ORDER BY | | |
| Scope | Global | Per-region | | |

---

## 🤔 Open Questions
- [ ] How to handle ties in ranking?
- [ ] How to support multiple leaderboards (daily/weekly/all-time)?
- [ ] How to shard Redis for very large leaderboards?
