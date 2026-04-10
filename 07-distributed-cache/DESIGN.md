# Design: Distributed Cache

## 🏗️ High-Level Architecture
```
Client → Cache Client (consistent hashing)
              ↓           ↓           ↓
           Node A      Node B      Node C
```

---

## 🔑 Key Components

### Consistent Hashing
- Hash ring with virtual nodes
- Minimizes key redistribution on node add/remove

### Replication
- Each key replicated to N successor nodes
- Handles node failures

---

## ⚖️ Design Decisions & Tradeoffs

| Decision | Option A | Option B | Chosen | Why |
|----------|----------|----------|--------|-----|
| Hashing | Consistent | Modulo | | |
| Replication | Sync | Async | | |
| Eviction | LRU | LFU | | |

---

## 🤔 Open Questions
- [ ] How many virtual nodes per physical node?
- [ ] How to detect and recover from node failure?
- [ ] How to handle hot keys (uneven load)?
