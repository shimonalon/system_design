# Project 9: Distributed File System

## 📌 Problem Statement
Design a simplified distributed file system (inspired by GFS/HDFS) that stores large files by splitting them into chunks, distributing chunks across storage nodes, and replicating each chunk for fault tolerance.

---

## ✅ Functional Requirements
- **Upload a file**: client uploads a file; system splits it into fixed-size chunks (e.g. 64MB)
- **Download a file**: client retrieves the file; system reassembles chunks in order
- **Delete a file**: remove all chunks of a file across all nodes
- **List files**: list all stored files with metadata (name, size, upload time)
- **Replication**: each chunk stored on 3 different nodes automatically
- **Fault recovery**: if a node goes down, under-replicated chunks are re-replicated automatically
- **Chunk integrity**: verify chunks with checksums (MD5/CRC32) to detect corruption

## 🚫 Non-Functional Requirements
- **Fault tolerant**: system continues working if up to 2 nodes fail (with replication factor 3)
- **Scalability**: add storage nodes without downtime
- **Throughput**: high sequential read/write throughput (optimized for large files, not small)
- **Consistency**: after a successful upload, all replicas must acknowledge before returning OK
- **Durability**: no data loss even after 1 node permanent failure

---

## 🔢 Estimations
- 1PB total storage across 100 nodes → 10TB per node
- Avg file size: 1GB → split into 16 chunks of 64MB
- Replication factor: 3 → effective storage = 3PB for 1PB of data
- Upload bandwidth per node: 1Gbps

---

## 🛠️ Recommended Tech Stack

| Layer | Technology | Why |
|-------|-----------|-----|
| **Master Node** | **Python** (FastAPI) | Track metadata: file → chunk mapping, chunk → node mapping |
| **Chunk Server** | **C++** | High-performance file I/O, handle concurrent chunk transfers |
| **Client** | **Python** | CLI client: split file, upload chunks, download + reassemble |
| **Metadata DB** | **PostgreSQL** | SQL: `files`, `chunks`, `chunk_locations` tables with FK constraints |
| **Checksum** | Python `hashlib` / C++ | Compute and verify MD5/CRC32 per chunk |
| **Stretch goal** | **TypeScript** | Build a web UI to browse and upload files |

### What you'll learn:
- File I/O in C++ (reading/writing binary chunks)
- PostgreSQL: multi-table joins, transactions for atomic metadata updates
- Replication protocol design (primary → replica acknowledgment)
- Heartbeat mechanism for detecting failed nodes

---

## 🔗 Resources
- [DESIGN.md](./DESIGN.md)
- `diagrams/`
- `src/`
