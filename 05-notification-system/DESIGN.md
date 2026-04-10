# Design: Notification System

## 🏗️ High-Level Architecture
```
Event Source → Notification Service → Message Queue
                                    → Push Worker   → APNs / FCM
                                    → Email Worker  → SendGrid
                                    → SMS Worker    → Twilio
```

---

## 🔑 Key Components
- **Event triggers**: User actions, system events
- **Preference Service**: User opt-in/opt-out per channel
- **Template Engine**: Personalized message rendering
- **Delivery Workers**: Per-channel handlers

---

## ⚖️ Design Decisions & Tradeoffs

| Decision | Option A | Option B | Chosen | Why |
|----------|----------|----------|--------|-----|
| Fan-out | Fan-out on write | Fan-out on read | | |
| Delivery guarantee | At-least-once | Best effort | | |

---

## 🤔 Open Questions
- [ ] How to handle unsubscribes in real time?
- [ ] How to retry failed deliveries per channel?
- [ ] How to prioritize urgent vs marketing notifications?
