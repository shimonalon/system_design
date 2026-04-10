# Design: Key-Value Store

## 🏗️ High-Level Architecture
```
Client → API Layer → In-Memory Hash Table
                   → Write-Ahead Log (WAL) → Disk
```

---

## 🔑 Key Components

### 1. Storage Engine
- [ ] In-memory HashMap
- [ ] LSM Tree (Log-Structured Merge)
- [ ] B-Tree

### 2. Persistence
- Write-Ahead Log (WAL)
- Periodic snapshots

### 3. Eviction Policy
- [ ] LRU (Least Recently Used)
- [ ] LFU (Least Frequently Used)
- [ ] TTL-based

---

## ⚖️ Design Decisions & Tradeoffs

| Decision | Option A | Option B | Chosen | Why |
|----------|----------|----------|--------|-----|
| Storage | In-memory | Disk-based | | |
| Persistence | WAL | Snapshots | | |
| Consistency | Strong | Eventual | | |

---

## 🤔 Open Questions
- [ ] How to handle data larger than RAM?
- [ ] How to replicate across nodes?
- [ ] How to handle concurrent writes?
