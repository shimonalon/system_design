# Project 3: Key-Value Store

## 📌 Problem Statement
Design and implement a simplified in-memory key-value store (like a mini Redis) that supports basic CRUD operations, TTL, and survives restarts via persistence.

---

## ✅ Functional Requirements
- `PUT(key, value)` — insert or overwrite a key
- `GET(key)` — retrieve a value by key; return null if not found or expired
- `DELETE(key)` — remove a key
- `TTL(key, seconds)` — set expiry on a key; auto-delete after TTL
- `EXISTS(key)` — check if a key is present and not expired
- `KEYS(pattern)` — list keys matching a glob pattern (e.g. `user:*`)

## 🚫 Non-Functional Requirements
- **Latency**: all operations O(1) average, < 1ms
- **Persistence**: survive process restarts (write-ahead log or snapshot)
- **Concurrency**: handle multiple simultaneous clients safely (thread-safe)
- **Memory efficiency**: configurable max memory with eviction when full
- **Correctness**: expired keys must never be returned

---

## 🔢 Estimations
- 1M keys stored in memory
- 100K ops/sec (mix of read/write)
- Average value size: 256 bytes → ~256MB RAM

---

## 🛠️ Recommended Tech Stack

| Layer | Technology | Why |
|-------|-----------|-----|
| **Core Store** | **C++** | This is the ideal C++ project — hash maps, memory management, threading |
| **Persistence** | Binary file / append-only log | Implement WAL yourself in C++ |
| **Client CLI** | **Python** | Write a simple TCP client in Python to talk to your C++ server |
| **Stretch goal** | **TypeScript** | Build a Node.js in-memory version using `Map<>` as a learning comparison |

### What you'll learn:
- C++ `std::unordered_map`, mutexes, condition variables
- TCP socket programming (server/client)
- Write-Ahead Log (WAL) design
- LRU cache eviction implementation in C++

---

## 🔗 Resources
- [DESIGN.md](./DESIGN.md)
- `diagrams/`
- `src/`
