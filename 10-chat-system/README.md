# Project 10: Chat System

## 📌 Problem Statement
Design a real-time messaging system (like WhatsApp) that supports 1-on-1 and group chats, with message persistence, delivery receipts, and online presence.

---

## ✅ Functional Requirements
- **Send a message**: user A sends a text message to user B (1-on-1)
- **Group messaging**: send a message to a group of up to 500 members
- **Message history**: load last N messages in a conversation (pagination)
- **Delivery receipts**: message states — sent ✓ / delivered ✓✓ / read ✓✓ (blue)
- **Online presence**: show whether a user is online or when they were last seen
- **Offline delivery**: messages sent while user is offline are delivered when they reconnect
- **Message ordering**: messages in a conversation appear in the correct order

## 🚫 Non-Functional Requirements
- **Latency**: message delivery < 100ms for online users
- **Availability**: 99.99% — users must always be able to send messages
- **Scalability**: 100M daily active users, 50B messages/day
- **Durability**: messages must be persisted — never lost even on server crash
- **Consistency**: within a conversation, message order must be consistent for all participants

---

## 🔢 Estimations
- 100M DAU, each sends 20 messages/day = 2B messages/day
- Peak: ~50K messages/sec
- Message size avg: 100 bytes → 200GB/day of new message data
- WebSocket connections: 100M persistent connections across server fleet

---

## 🛠️ Recommended Tech Stack

| Layer | Technology | Why |
|-------|-----------|-----|
| **WebSocket Server** | **Python** (`websockets` / FastAPI WebSocket) | Handle real-time bidirectional connections |
| **Message Store** | **PostgreSQL** | Practice SQL: `conversations`, `messages`, `receipts` tables |
| **Presence Store** | **Redis** | TTL keys: `online:{user_id}` expires after 30s of inactivity |
| **Message Queue** | **Redis** pub/sub | Fan-out messages to group members |
| **Stretch goal** | **TypeScript** (React) | Build the chat UI — WebSocket client in the browser |
| **Stretch goal 2** | **C++** | Implement a high-performance WebSocket server to replace Python |

### What you'll learn:
- WebSocket protocol and connection lifecycle
- SQL: designing time-series-like `messages` table with pagination using `LIMIT`/`OFFSET` or cursor-based
- Redis pub/sub for fan-out to online users
- Handling offline message queuing and delivery on reconnect

---

## 🔗 Resources
- [DESIGN.md](./DESIGN.md)
- `diagrams/`
- `src/`
