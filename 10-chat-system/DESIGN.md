# Design: Chat System

## 🏗️ High-Level Architecture
```
Client A ←→ WebSocket Server ←→ Message Queue → Client B
                   ↓
            Message DB (Cassandra)
            Presence Service (Redis)
```

---

## 🔑 Key Components
- **WebSocket**: Persistent connection for real-time messaging
- **Message Store**: Cassandra (write-heavy, time-series)
- **Presence**: Redis TTL keys for online status
- **Group Chat**: Fan-out to all group members

---

## ⚖️ Design Decisions & Tradeoffs

| Decision | Option A | Option B | Chosen | Why |
|----------|----------|----------|--------|-----|
| Protocol | WebSocket | Long polling | | |
| Storage | Cassandra | MySQL | | |
| Message ID | UUID | Snowflake ID | | |

---

## 🤔 Open Questions
- [ ] How to deliver messages to offline users?
- [ ] How to handle message ordering in group chats?
- [ ] How to scale WebSocket servers?
