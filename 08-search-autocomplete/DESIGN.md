# Design: Search Autocomplete

## 🏗️ High-Level Architecture
```
Client → API Server → Redis (prefix cache)
                    → Trie Service
                    → Search Index (offline build)
```

---

## 🔑 Key Components

### Trie (Prefix Tree)
- Each node = one character
- Leaf nodes store top-K suggestions + scores
- Updated periodically via batch job

### Caching
- Cache popular prefixes in Redis
- Refresh cache on schedule

---

## ⚖️ Design Decisions & Tradeoffs

| Decision | Option A | Option B | Chosen | Why |
|----------|----------|----------|--------|-----|
| Data structure | Trie | Inverted Index | | |
| Update frequency | Real-time | Batch | | |
| Storage | In-memory | Disk-backed | | |

---

## 🤔 Open Questions
- [ ] How to handle typos / fuzzy matching?
- [ ] How to personalize suggestions per user?
- [ ] How to shard the trie across servers?
