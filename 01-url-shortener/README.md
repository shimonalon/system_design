# Project 1: URL Shortener

## 📌 Problem Statement
Design a URL shortening service like bit.ly that converts long URLs into short, unique aliases.

---

## ✅ Functional Requirements
- Given a long URL, generate a short unique URL (e.g. `short.ly/aB3xQ`)
- Redirect user to the original URL when the short URL is accessed
- Short codes must be unique and collision-free
- Custom aliases: user can request a specific short code
- URL expiration: URLs can have an optional TTL after which they return 404
- Basic analytics: track how many times a short URL was clicked

## 🚫 Non-Functional Requirements
- **Availability**: 99.99% uptime (redirects must always work)
- **Latency**: redirect must complete in < 10ms (cache hit) / < 50ms (cache miss)
- **Scalability**: support 100M stored URLs, 4000 redirects/sec
- **Durability**: no URL should be silently lost
- **Security**: prevent abuse (malicious URL submission)

---

## 🔢 Estimations
- Read/Write ratio: 100:1
- 100M new URLs/month → ~40 writes/sec
- 10B redirects/month → ~4000 reads/sec
- Storage: avg URL = 500 bytes → 100M × 500B = ~50GB

---

## 🛠️ Recommended Tech Stack

| Layer | Technology | Why |
|-------|-----------|-----|
| **API Server** | **Python** (FastAPI) | You know Python; FastAPI is async & great for REST APIs |
| **Database** | **PostgreSQL** | Practice SQL — store URLs, aliases, expiry |
| **Cache** | **Redis** | Key-value store for short_code → long_url lookup |
| **ID Generation** | Python (Base62 encode) | Simple to implement yourself |
| **Stretch goal** | **TypeScript** (Node/Express) | Re-implement the API layer in TS for practice |

### What you'll learn:
- Writing SQL schemas, indexes, constraints
- Redis `SET`/`GET`/`EXPIRE` commands
- REST API design with FastAPI
- HTTP 301 vs 302 redirects

---

## 🔗 Resources
- [DESIGN.md](./DESIGN.md) — Architecture & decisions
- `diagrams/` — Architecture diagrams
- `src/` — Implementation
