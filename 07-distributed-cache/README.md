# Project 7: Distributed Cache

## 📌 Problem Statement
Design a distributed caching system (like Memcached) that partitions data across multiple cache nodes using consistent hashing, so the system can scale horizontally and survive individual node failures.

---

## ✅ Functional Requirements
- `GET(key)` — retrieve a cached value; return null on miss
- `SET(key, value, ttl)` — store a value with optional expiry
- `DELETE(key)` — evict a key from the cache
- **Consistent hashing**: keys are deterministically distributed across N nodes
- **Node discovery**: clients automatically know which node owns which key
- **Replication**: each key is replicated to R successor nodes (default R=2)
- **Graceful node add/remove**: only ~1/N keys are remapped when a node joins/leaves

## 🚫 Non-Functional Requirements
- **Latency**: < 1ms for cache hits
- **Availability**: if one node fails, replicated keys are served from replicas
- **Scalability**: add nodes without downtime or full cache invalidation
- **Consistency**: eventual consistency is acceptable (replicas may lag briefly)
- **Memory**: each node enforces a max memory limit with LRU eviction

---

## 🔢 Estimations
- 5 cache nodes, each with 8GB RAM
- Total cache: 40GB
- 500K requests/sec total → 100K req/sec per node
- Average value size: 1KB → 40M cached entries

---

## 🛠️ Recommended Tech Stack

| Layer | Technology | Why |
|-------|-----------|-----|
| **Cache Node Server** | **C++** | High-performance in-memory store — ideal C++ project |
| **Consistent Hash Ring** | **C++** | Implement the hash ring + virtual nodes in C++ |
| **Client Library** | **Python** | Python client that does hashing and routes to correct node |
| **Node Communication** | TCP sockets | Implement a simple binary or text protocol |
| **Stretch goal** | **TypeScript** | Build a JS client library for the cache |

### What you'll learn:
- Consistent hashing algorithm & virtual nodes
- C++ networking (TCP sockets, `epoll`/`select`)
- LRU eviction using `std::list` + `std::unordered_map` in C++
- Replication and handling node failure

---

## 🔗 Resources
- [DESIGN.md](./DESIGN.md)
- `diagrams/`
- `src/`
