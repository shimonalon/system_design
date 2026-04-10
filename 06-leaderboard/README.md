# Project 6: Leaderboard System

## 📌 Problem Statement
Design a real-time leaderboard for a gaming platform that displays player rankings by score, supports multiple leaderboard scopes (daily, weekly, all-time), and handles millions of concurrent players.

---

## ✅ Functional Requirements
- **Submit score**: update a player's score (scores are cumulative or absolute — define which)
- **Get top-N players**: return the top 10/100 players with their scores and ranks
- **Get player rank**: return the rank and score of a specific player
- **Multiple leaderboards**: support daily, weekly, all-time scopes independently
- **Tie-breaking**: players with equal scores ranked by who achieved it first (timestamp)
- **Player profile**: each rank entry shows player ID, display name, score, and rank

## 🚫 Non-Functional Requirements
- **Latency**: rank reads < 10ms, score updates < 20ms
- **Real-time**: leaderboard reflects score updates within 1 second
- **Scale**: 10M active players, 5000 score updates/sec
- **Consistency**: rank reads should be eventually consistent (1–2 sec lag is OK)
- **Availability**: 99.9% uptime — a Redis failure must not lose scores (fall back to DB)

---

## 🔢 Estimations
- 10M players
- 5000 writes/sec (score updates)
- 50K reads/sec (top-10 fetches, rank lookups)
- Redis ZSET memory: 10M entries × ~64 bytes ≈ ~640MB per leaderboard

---

## 🛠️ Recommended Tech Stack

| Layer | Technology | Why |
|-------|-----------|-----|
| **API Server** | **Python** (FastAPI) | REST endpoints for score submit and rank fetch |
| **Leaderboard Store** | **Redis Sorted Sets (ZSET)** | Native O(log N) ranking — exactly built for this |
| **Persistent Storage** | **PostgreSQL** | Backup scores, player profiles, historical data |
| **Schema Practice** | SQL | Design `players`, `scores`, `leaderboard_snapshots` tables |
| **Stretch goal** | **TypeScript** | Build a live leaderboard UI with React that polls the API |
| **Stretch goal 2** | **C++** | Implement a Skiplist (the data structure Redis ZSET uses) from scratch |

### What you'll learn:
- Redis `ZADD`, `ZREVRANK`, `ZREVRANGE`, `ZINCRBY`
- SQL: composite indexes, `RANK()` window function
- How to sync Redis ↔ PostgreSQL (write-through vs write-behind)
- Real-time UI updates with polling or WebSocket

---

## 🔗 Resources
- [DESIGN.md](./DESIGN.md)
- `diagrams/`
- `src/`
