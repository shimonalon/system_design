# Project 1: URL Shortener

## 📌 Problem Statement
Design a URL shortening service like bit.ly that converts long URLs into short, unique aliases.

---

## ✅ MVP Requirements
- Generate short unique URLs from long URLs
- Redirect short URLs to originals
- Ensure collision-free short codes
- Track click counts

---

## 📁 Project Structure

```
01-url-shortener/
├── DESIGN.md                    ← System architecture
├── README.md                    ← This file
├── .gitignore
│
├── backend/                     ← Python + FastAPI
│   ├── src/                     ← Application code
│   ├── tests/                   ← Unit & integration tests
│   ├── requirements.txt
│   ├── Dockerfile
│   ├── .env.example
│   ├── pytest.ini
│   └── SETUP.md                 ← Start here!
│
└── frontend/                    ← TypeScript + React (Phase 5)
    ├── src/
    ├── public/
    ├── package.json
    ├── vite.config.ts
    ├── Dockerfile
    ├── .env.example
    └── SETUP.md
```

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|-----------|
| API | Python + FastAPI |
| Database | PostgreSQL |
| Cache | Redis |
| Frontend | TypeScript + React + Vite (Phase 5) |

---

## 📚 Documentation

- **[DESIGN.md](./DESIGN.md)** — System design & algorithms
- **[PROJECT_STRUCTURE.md](./PROJECT_STRUCTURE.md)** — How files are organized
- **[backend/SETUP.md](./backend/SETUP.md)** — Backend setup & implementation
- **[frontend/SETUP.md](./frontend/SETUP.md)** — Frontend setup (Phase 5)

---

## 🎯 Implementation Phases

| Phase | Status | Deliverable |
|-------|--------|-------------|
| **1. Design** | ✅ Done | [DESIGN.md](./DESIGN.md) |
| **2. Setup** | ✅ Done | Scaffolding + function declarations |
| **3. Implementation** | 🚀 Next | Implement backend functions |
| **4. Testing** | ⏳ Later | Unit + integration tests |
| **5. Frontend** | ⏳ Later | React UI (stretch goal) |

---

## 🚀 Getting Started

1. **Read the design**: `DESIGN.md`
2. **Go to backend**: `cd backend && cat SETUP.md`
3. **Implement functions**: Follow the TODO comments
4. **Run tests**: `pytest`
5. **Start server**: `uvicorn src.main:app --reload`

---

## ✅ Success Criteria

- ✅ Short URL generation works
- ✅ Redirects work (< 50ms)
- ✅ Click tracking works
- ✅ No collisions
- ✅ Tests passing
- ✅ Can run with Docker
