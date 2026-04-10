# Design: URL Shortener

## 🏗️ High-Level Architecture
> Add your diagram here (Excalidraw / draw.io export)

```
Client → Load Balancer → App Servers → Cache (Redis)
                                     ↓
                                  Database (PostgreSQL)
```

---

## 🔑 Key Components

### 1. Shortening Algorithm
- [ ] Approach chosen: (MD5 / Base62 / Counter-based)
- Tradeoffs:

### 2. Database Schema
```sql
-- urls table
id          BIGINT PRIMARY KEY
short_code  VARCHAR(10) UNIQUE
long_url    TEXT
created_at  TIMESTAMP
expires_at  TIMESTAMP
```

### 3. Caching Strategy
- Cache: Redis
- TTL: ?
- Eviction policy: LRU

### 4. Redirect Flow
1. Client hits `short.ly/abc123`
2. Check Redis cache
3. If miss → query DB
4. Return HTTP 301/302 redirect

---

## ⚖️ Design Decisions & Tradeoffs

| Decision | Option A | Option B | Chosen | Why |
|----------|----------|----------|--------|-----|
| Redirect type | 301 (permanent) | 302 (temporary) | | |
| ID generation | UUID | Base62 counter | | |
| Storage | SQL | NoSQL | | |

---

## 🤔 Open Questions
- [ ] How to handle hash collisions?
- [ ] How to scale the ID generator across nodes?
- [ ] Do we need analytics (click tracking)?
