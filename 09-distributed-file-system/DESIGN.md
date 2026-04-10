# Design: Distributed File System

## 🏗️ High-Level Architecture
```
Client → Master Node (metadata) → Chunk Servers (data)
                ↓
         Metadata DB (file→chunk mapping)
```

---

## 🔑 Key Components
- **Master Node**: Tracks file metadata, chunk locations
- **Chunk Servers**: Store actual file chunks (e.g. 64MB each)
- **Replication**: Each chunk stored on 3 nodes

### Upload Flow
1. Client sends file to Master
2. Master assigns chunk IDs + chunk servers
3. Client streams chunks directly to chunk servers
4. Chunk servers replicate to peers

---

## ⚖️ Design Decisions & Tradeoffs

| Decision | Option A | Option B | Chosen | Why |
|----------|----------|----------|--------|-----|
| Chunk size | 64MB | 4MB | | |
| Replication factor | 3 | 2 | | |
| Master | Single | Distributed | | |

---

## 🤔 Open Questions
- [ ] How to detect and re-replicate lost chunks?
- [ ] How to handle Master node failure?
- [ ] How to support file versioning?
