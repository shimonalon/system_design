# URL Shortener — System Design Document

## 1. Problem Analysis

### Functional Requirements (MVP)
- ✅ Generate short URL from long URL
- ✅ Redirect short URL to original long URL  
- ✅ Ensure short codes are unique & collision-free
- ✅ Basic analytics: track click count per URL

### Non-Functional Requirements
- **Availability**: 99.99% uptime
- **Latency**: < 10ms (cache hit), < 50ms (cache miss)
- **Scalability**: 100M stored URLs, 4000 redirects/sec
- **Durability**: no URL loss
- **Security**: prevent abuse

---

## 2. Capacity Estimations

| Metric | Calculation | Value |
|--------|-------------|-------|
| **Write Rate** | 100M URLs/month ÷ (30 × 86400 sec) | ~40 writes/sec |
| **Read Rate** | 10B redirects/month ÷ (30 × 86400 sec) | ~4000 reads/sec |
| **Read/Write Ratio** | 4000 / 40 | **100:1** |
| **Storage (URLs)** | 100M × 500B avg per entry | ~50 GB |
| **Total Storage** | URLs + metadata | ~60 GB |
| **Cache Size** | 20% of URLs cached | ~10 GB |
| **Base62 Length** | 62^5 = 915M possible codes | **5 chars sufficient** |

### Why These Numbers Matter
- 40 writes/sec is easy for PostgreSQL (can handle 1000s/sec)
- 4000 reads/sec means **we MUST cache** (Redis)
- 60 GB storage fits in single machine
- 5-char Base62 codes cover 915M URLs (safe for 100M)

---

## 3. System Architecture

### High-Level Diagram

```
┌─────────────────────────────────────────────────────┐
│                    Client/Browser                    │
└────────┬────────────────────────────────┬────────────┘
         │                                │
    POST /api/shorten              GET /:short_code
         │                                │
         ▼                                ▼
┌─────────────────────────────────────────────────────┐
│            FastAPI Server (Python)                   │
│  • POST /api/shorten                                │
│  • GET /:short_code                                 │
│  • GET /api/stats/:short_code                       │
└────────┬──────────────────────────────┬──────────────┘
         │                              │
    (Check cache)                 (Increment clicks)
         │                              │
         ▼                              ▼
    ┌─────────────┐          ┌──────────────────┐
    │   Redis     │          │   PostgreSQL     │
    │  Cache      │          │   Persistent DB  │
    │  < 10ms     │          │  < 50ms          │
    └─────────────┘          └──────────────────┘
```

### Request Flow: POST /api/shorten

```
1. Receive: { "long_url": "https://example.com/very/long/path" }

2. Validate:
   - Is URL HTTP/HTTPS?
   - Is length reasonable (< 2048)?

3. Insert into DB:
   INSERT INTO urls (long_url, created_at)
   → Database auto-generates: id = 1000

4. Generate short code:
   Convert id 1000 → Base62 "rs"

5. Update row:
   UPDATE urls SET short_code = 'rs' WHERE id = 1000

6. Cache it:
   Redis SET "rs" → "https://example.com/..." (TTL 24h)

7. Return:
   { "short_code": "rs", "short_url": "http://short.ly/rs" }
```

### Request Flow: GET /:short_code (Redirect)

```
1. Receive: GET /rs

2. Check Redis cache:
   cached = Redis GET "rs"
   IF found → Jump to step 6

3. Query database:
   SELECT long_url FROM urls WHERE short_code = 'rs'

4. Check if expired:
   IF expires_at < NOW() → Return 404
   ELSE → Continue

5. Increment clicks (async, non-blocking):
   UPDATE urls SET click_count = click_count + 1
   (Fire and forget - don't wait)

6. Return redirect:
   HTTP 302 Found
   Location: https://example.com/...
```

### Request Flow: GET /api/stats/:short_code

```
1. Query database:
   SELECT short_code, long_url, created_at, click_count
   FROM urls
   WHERE short_code = 'rs'

2. Return JSON:
   { "short_code": "rs", "long_url": "...", "click_count": 42 }
```

---

## 4. Database Schema

### Table: urls

```sql
CREATE TABLE urls (
  -- Primary Key
  id BIGSERIAL PRIMARY KEY,
  
  -- Short Code
  short_code VARCHAR(10) UNIQUE NOT NULL,
  
  -- Original URL
  long_url TEXT NOT NULL CHECK (long_url ~ '^https?://'),
  
  -- Timestamps
  created_at TIMESTAMP DEFAULT NOW(),
  expires_at TIMESTAMP,  -- NULL = never expires
  
  -- Analytics
  click_count INT DEFAULT 0,
  
  -- Future: Multi-user support
  user_id VARCHAR(255)
);

-- Indexes
CREATE INDEX idx_short_code ON urls(short_code);
CREATE INDEX idx_expires_at ON urls(expires_at) 
  WHERE expires_at IS NOT NULL;
CREATE INDEX idx_user_id_created ON urls(user_id, created_at);
```

### Column Decisions

| Column | Type | Why |
|--------|------|-----|
| `id` | BIGSERIAL | Auto-incrementing; used for Base62 generation |
| `short_code` | VARCHAR(10) UNIQUE | Max 10 chars sufficient for Base62; UNIQUE enforces no duplicates |
| `long_url` | TEXT | URLs can exceed 2048 chars; CHECK ensures HTTP/HTTPS only |
| `created_at` | TIMESTAMP | Track when URL was shortened |
| `expires_at` | TIMESTAMP NULL | For future TTL feature; NULL = never expires |
| `click_count` | INT | Track analytics; updated async |
| `user_id` | VARCHAR(255) | For future multi-user feature |

### Index Strategy

| Index | Query | Why |
|-------|-------|-----|
| `idx_short_code` | `WHERE short_code = 'rs'` | **CRITICAL**: Every redirect uses this |
| `idx_expires_at` | `WHERE expires_at < NOW()` | Cleanup job to find expired URLs |
| `idx_user_id_created` | `WHERE user_id = '...' ORDER BY created_at` | Future: list user's URLs |

---

## 5. Short Code Generation: Base62 Algorithm

### Why Base62?

| Method | Alphabet | Example (ID=1000) | Pros | Cons |
|--------|----------|-------------------|------|------|
| **Base10** | 10 | "1000" | Simple | Long (4 chars) |
| **Base16** | 16 | "3e8" | Familiar | Still 3 chars |
| **Base62** | 62 | "rs" | ✅ Compact | Slightly complex |
| **UUID** | N/A | "550e8400..." | Random | 36 chars |

**Winner: Base62** — most compact without collisions

### Base62 Alphabet

```
Index:  0-9    10-35  36-61
Char:   0-9    a-z    A-Z

Example:
0 → '0'
9 → '9'
10 → 'a'
35 → 'z'
36 → 'A'
61 → 'Z'
62 → '10' (like decimal overflow)
```

### Encoding Algorithm

```python
def encode_base62(num: int) -> str:
    if num == 0:
        return "0"
    
    alphabet = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    result = []
    
    while num > 0:
        result.append(alphabet[num % 62])
        num //= 62
    
    return ''.join(reversed(result))

# Examples:
# 0 → "0"
# 1 → "1"
# 9 → "9"
# 10 → "a"
# 61 → "Z"
# 62 → "10"
# 100 → "1w"
# 1000 → "rs"
# 1000000 → "4c92"
```

### Decoding Algorithm

```python
def decode_base62(code: str) -> int:
    alphabet = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    result = 0
    
    for char in code:
        result = result * 62 + alphabet.index(char)
    
    return result
```

### Capacity Analysis

```
Length  Max IDs       Real-world URLs
1       62            62
2       3,844         ~3K
3       238,328       ~238K
4       14.8M         ~14M
5       915M          ~915M  ← Covers 100M URLs ✅
6       56.8B         ~57B   ← Extra safety margin

Conclusion: 5 chars max for 100M+ URLs
```

---

## 6. Caching Strategy

### Cache Flow

```
GET /rs
  │
  ├─► Redis GET "rs"
  │     │
  │     ├─ Found? ────► Return (< 10ms)
  │     │
  │     └─ Miss
  │
  ├─► PostgreSQL Query
  │     │
  │     ├─ Found? ──► Cache in Redis ──► Return (< 50ms)
  │     │
  │     └─ Not Found ──► Return 404
```

### Redis Operations

```python
# After successful INSERT in DB:
redis.set(
    key=short_code,        # "rs"
    value=long_url,        # "https://example.com/..."
    ex=86400               # TTL: 24 hours
)

# On redirect request:
cached = redis.get(short_code)
if cached:
    return redirect(cached)  # < 10ms ✅
else:
    # Query DB and cache
    url = db.get_url(short_code)
    redis.set(short_code, url, ex=86400)
    return redirect(url)

# On URL deletion:
redis.delete(short_code)
```

### Performance Analysis

```
Assumptions:
- 80% of requests hit cache
- Cache hit latency: 10ms (Redis)
- Cache miss latency: 50ms (PostgreSQL)

Average latency:
0.8 × 10ms + 0.2 × 50ms = 18ms ✅

Meets requirement: < 50ms p99
```

### Cache Invalidation

**Strategy**: Time-based TTL (24 hours)

✅ **Pros:**
- Simple: Redis auto-deletes after TTL
- No complex invalidation logic
- Automatic cleanup

⚠️ **Cons:**
- 24-hour stale data window
- If URL deleted from DB, cache still serves for up to 24h

**Mitigation:**
- When URL is deleted/expired: manually `redis.delete(short_code)`
- Monitor cache hit rate
- Eventual consistency is acceptable for this use case

---

## 7. API Specifications

### POST /api/shorten

```
Request:
POST /api/shorten
Content-Type: application/json

{
  "long_url": "https://www.example.com/path/to/very/long/url"
}

Response 201 Created:
{
  "short_code": "rs",
  "short_url": "http://short.ly/rs",
  "created_at": "2026-04-17T10:30:00Z"
}

Error 400 Bad Request:
{
  "error": "Invalid URL format",
  "details": "URL must start with http:// or https://"
}

Error 500 Internal Server Error:
{
  "error": "Failed to generate short code"
}
```

### GET /:short_code

```
Request:
GET /rs

Response 302 Found:
HTTP/1.1 302 Found
Location: https://www.example.com/path/to/very/long/url

(Browser automatically follows redirect)

Error 404 Not Found:
{
  "error": "Short code not found or expired"
}
```

### GET /api/stats/:short_code

```
Request:
GET /api/stats/rs

Response 200 OK:
{
  "short_code": "rs",
  "long_url": "https://www.example.com/path/to/very/long/url",
  "created_at": "2026-04-17T10:30:00Z",
  "click_count": 42
}

Error 404 Not Found:
{
  "error": "Short code not found"
}
```

---

## 8. Design Decisions & Tradeoffs

### Decision 1: Counter + Base62 vs. UUID

| Aspect | Counter + Base62 | UUID + Base62 |
|--------|------------------|---------------|
| **Collision Risk** | ✅ Zero (guaranteed) | ✅ ~0 (1 in trillions) |
| **Code Length** | ✅ 4-6 chars | ❌ 22 chars |
| **Generation** | ✅ Fast | ✅ Fast |
| **Predictability** | ❌ Sequential (1,2,3...) | ✅ Random |
| **Distributed** | ❌ Needs coordinator | ✅ Works standalone |
| **Single DB** | ✅ Works fine | ✅ Works fine |

**Decision: Counter + Base62 for MVP** ✅
- Simplest implementation
- Zero collisions by design
- PostgreSQL handles 40 writes/sec easily

---

### Decision 2: HTTP 302 vs. 301 Redirect

| Aspect | 302 Temporary | 301 Permanent |
|--------|---------------|---------------|
| **Browser Cache** | ❌ Doesn't cache | ✅ Caches locally |
| **Server Load** | ❌ Every hit | ✅ Fewer hits |
| **Target Changes** | ✅ Easy to change | ❌ Browser won't update |
| **Analytics** | ✅ All clicks tracked | ⚠️ May miss cached |

**Decision: 302 Temporary for MVP** ✅
- Flexibility if we need to change targets
- Easier click tracking
- Browser cache overhead is negligible at 4000 req/sec

---

### Decision 3: Cache All URLs vs. Cache Popular Only

| Aspect | Cache All | Cache Popular |
|--------|-----------|----------------|
| **Memory** | ❌ ~10 GB | ✅ Smaller |
| **Latency** | ✅ < 10ms all | ⚠️ Variable |
| **Complexity** | ✅ Simple TTL | ❌ Scoring logic |
| **Hit Rate** | ✅ 80%+ | ⚠️ Variable |

**Decision: Cache All with 24h TTL** ✅
- Simpler to implement
- 10 GB is reasonable for modern servers
- Most URLs are accessed multiple times

---

### Decision 4: Custom Aliases in MVP

**Decision: Exclude from MVP** ✅
- Adds complexity (collision checking)
- Keep MVP focused on core feature
- Add in v1.1 as stretch goal

---

### Decision 5: URL Expiration in MVP

**Decision: Exclude from MVP** ✅
- Database schema supports it (`expires_at`)
- No cleanup job needed yet
- Can add later without schema changes
- MVP philosophy: "URLs live forever"

---

## 9. Failure Scenarios

### Scenario 1: Redis is Down

```
Impact: Cache layer unavailable

Mitigation:
1. Catch Redis connection error
2. Fall back to PostgreSQL query
3. Skip cache write
4. Log error

Result:
- Latency increases: 10ms → 50ms
- Service degrades but still works ✅
- No data loss ✅
```

### Scenario 2: PostgreSQL is Down

```
Impact: Database unreachable

Mitigation:
1. Return 503 Service Unavailable
2. No fallback (need DB to function)

Result:
- All requests fail ❌
- Violates 99.99% SLA

Prevention (future):
- Multi-region replication
- Automated failover (Patroni)
- Regular backups
```

### Scenario 3: Duplicate Short Code

```
Problem: Two threads insert same short_code

Prevention:
- Database UNIQUE constraint on short_code
- One succeeds, other gets UNIQUE_VIOLATION
- Retry logic generates next ID

Why unlikely:
- Counter is sequential
- Each ID maps to one code
- No race condition ✅
```

---

## 10. Monitoring & Metrics

### Key Metrics to Track

```
Latency:
- Cache hit latency (target: < 10ms)
- Cache miss latency (target: < 50ms)
- p50, p95, p99 latencies

Throughput:
- Writes/sec (target: 40+)
- Reads/sec (target: 4000+)
- Cache hit rate (target: 80%+)

Availability:
- Uptime % (target: 99.99%)
- Error rate by type

Resource Usage:
- PostgreSQL: connection pool, query time
- Redis: memory, hit rate, evictions
- API server: CPU, memory
```

### Alerts to Set

- Cache hit rate < 70%
- Average latency > 50ms
- Redis memory > 8 GB
- Database query time > 100ms
- Error rate > 0.1%

---

## 11. Future Enhancements (v1.1+)

1. **Custom Aliases**
   - Allow users to request specific short codes
   - Collision detection
   - Reserved words list

2. **URL Expiration**
   - Add TTL parameter on shorten
   - Cleanup background job
   - Return 410 Gone when expired

3. **Rate Limiting**
   - Prevent abuse
   - IP-based throttling
   - API key quotas

4. **Analytics Dashboard**
   - Click trends over time
   - Top URLs
   - Geographic distribution

5. **Multi-user Support**
   - User authentication
   - API keys
   - Per-user URL list

6. **QR Code Generation**
   - Generate QR code endpoint
   - SVG or PNG format

---

## 12. Deployment Checklist

- [ ] PostgreSQL setup & migration
- [ ] Redis setup & configuration
- [ ] FastAPI server development
- [ ] Unit tests (Base62, URL validation)
- [ ] Integration tests (full flows)
- [ ] Docker setup (API, DB, Cache)
- [ ] Docker Compose for local dev
- [ ] Load testing (4000 req/sec)
- [ ] Monitoring & alerting setup
- [ ] Documentation & API docs
