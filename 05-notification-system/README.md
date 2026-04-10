# Project 5: Notification System

## 📌 Problem Statement
Design a notification system that delivers messages to users across multiple channels (push, email, SMS) based on user preferences and triggered events.

---

## ✅ Functional Requirements
- **Trigger a notification**: any service can emit an event (e.g. "order shipped")
- **Multi-channel delivery**: send via push notification, email, and/or SMS
- **User preferences**: each user can enable/disable specific channels per notification type
- **Template rendering**: notifications use templates with dynamic variables (e.g. `Hello {{name}}`)
- **Bulk notifications**: send to millions of users (e.g. marketing broadcast)
- **Delivery tracking**: track sent / delivered / failed status per notification
- **Do-Not-Disturb**: respect quiet hours per user timezone

## 🚫 Non-Functional Requirements
- **Throughput**: 1M notifications/hour for bulk sends
- **Latency**: push notifications delivered in < 1 second
- **Reliability**: at-least-once delivery — never silently drop a notification
- **Fault tolerant**: if email provider is down, queue and retry
- **Scalability**: add new channels (e.g. Slack, Telegram) without changing core logic

---

## 🔢 Estimations
- 10M users, avg 5 notifications/day = 50M notifications/day
- Peak: ~600 notifications/sec
- Email ~60%, Push ~30%, SMS ~10%

---

## 🛠️ Recommended Tech Stack

| Layer | Technology | Why |
|-------|-----------|-----|
| **Notification API** | **Python** (FastAPI) | Accept trigger events from other services |
| **Message Queue** | **Redis** (pub/sub or lists) | Decouple producers from channel workers |
| **Email Worker** | **Python** | Call SendGrid/Mailgun API |
| **Push Worker** | **Python** | Call FCM (Firebase Cloud Messaging) |
| **User Preferences DB** | **PostgreSQL** | SQL: store user channel preferences, quiet hours |
| **Delivery Log** | **PostgreSQL** | Track status of every notification |
| **Stretch goal** | **TypeScript** | Build the frontend preferences UI in React/TS |

### What you'll learn:
- Pub/Sub pattern with Redis
- SQL: designing a `notifications` table with status enum, foreign keys
- Fan-out patterns for bulk delivery
- External API integration (SendGrid, FCM)

---

## 🔗 Resources
- [DESIGN.md](./DESIGN.md)
- `diagrams/`
- `src/`
