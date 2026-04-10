# Project 11: Feed System

## 📌 Problem Statement
Design a social media news feed (like Twitter/Instagram timeline) that shows a user the recent posts of everyone they follow, sorted by recency or relevance.

---

## ✅ Functional Requirements
- **Create a post**: user publishes a text post (with optional media URL)
- **Follow / Unfollow**: user A follows/unfollows user B
- **Home timeline**: user sees an ordered feed of posts from all followed users
- **Pagination**: load feed in pages (e.g. 20 posts per page, infinite scroll)
- **Like a post**: users can like posts; like count is visible
- **Delete a post**: remove a post; it must disappear from all followers' feeds
- **User profile feed**: view all posts by a specific user

## 🚫 Non-Functional Requirements
- **Latency**: home timeline loads in < 200ms
- **Scalability**: 500M users, 200M DAU, 10M posts/day
- **Availability**: 99.99% — feed must always load (even if slightly stale)
- **Eventual consistency**: new posts may take up to 5 seconds to appear in followers' feeds
- **Storage**: posts retained indefinitely; old posts accessible via pagination

---

## 🔢 Estimations
- 200M DAU, avg 2 timeline loads/day = 400M timeline requests/day → ~5000 req/sec
- 10M posts/day → ~115 writes/sec
- Avg user follows 300 people → fan-out of 300 writes per post = 3450 writes/sec
- Feed cache per user: 20 post IDs × 8 bytes × 200M users = ~32GB (only cache active users)

---

## 🛠️ Recommended Tech Stack

| Layer | Technology | Why |
|-------|-----------|-----|
| **API Server** | **Python** (FastAPI) | Post creation, follow graph, timeline endpoints |
| **Feed Cache** | **Redis** (sorted set or list) | Pre-computed timeline per user: `LPUSH feed:{user_id} post_id` |
| **Post Storage** | **PostgreSQL** | `posts`, `follows`, `likes` tables — rich SQL practice |
| **Fan-out Worker** | **Python** (async worker) | On post creation, push post ID to all followers' feed caches |
| **Stretch goal** | **TypeScript** (React) | Build the feed UI with infinite scroll |
| **Stretch goal 2** | **C++** | Implement the fan-out engine for ultra-high throughput |

### What you'll learn:
- SQL: `follows` join table, `EXPLAIN` for query optimization, pagination patterns
- Redis lists/sorted sets for feed storage
- Fan-out on write vs fan-out on read tradeoff (key system design concept)
- Handling celebrities (10M followers) as a special case

---

## 🔗 Resources
- [DESIGN.md](./DESIGN.md)
- `diagrams/`
- `src/`
