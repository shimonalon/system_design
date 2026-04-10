# Project 8: Search Autocomplete

## 📌 Problem Statement
Design a search autocomplete (typeahead) system that returns the top-5 query suggestions as a user types, ranked by popularity, with sub-100ms response time.

---

## ✅ Functional Requirements
- Given a prefix string, return top-5 suggested completions
- Suggestions ranked by **search frequency** (most searched = first)
- Support **incremental updates**: new popular searches appear in suggestions over time
- Case-insensitive matching
- Support for filtering suggestions per category (e.g. "movies", "products")
- **Search logging**: every search query is recorded for frequency analysis

## 🚫 Non-Functional Requirements
- **Latency**: return suggestions in < 100ms (ideally < 20ms from cache)
- **High read throughput**: 10K suggestion requests/sec
- **Eventual consistency**: new trending queries appear in suggestions within 1 hour
- **Scalability**: support 10M unique queries in the index
- **Availability**: 99.9% — users should always get some suggestions

---

## 🔢 Estimations
- 10B searches/day → ~115K searches/sec
- Each keystroke = 1 autocomplete request → avg 5 keystrokes = 500K req/sec
- Top 1M prefixes cover ~80% of traffic (cache these)
- Trie size: 10M unique queries × avg 20 chars = ~200MB

---

## 🛠️ Recommended Tech Stack

| Layer | Technology | Why |
|-------|-----------|-----|
| **Trie / Index** | **C++** | Build the Trie data structure in C++ — great DS exercise |
| **Prefix Cache** | **Redis** | Cache top-5 results per prefix with `SET key json_array` |
| **Query Log** | **PostgreSQL** | Log all searches; run batch job to compute frequencies |
| **API Server** | **Python** (FastAPI) | Serve suggestions, query Redis first, fall back to Trie |
| **Batch Rebuilder** | **Python** | Scheduled job: read query logs → rebuild Trie + warm cache |
| **Stretch goal** | **TypeScript** | Build the live search UI in React with debounced input |

### What you'll learn:
- Trie data structure implementation in C++
- Redis as an application-level cache with JSON values
- SQL aggregate queries: `SELECT query, COUNT(*) GROUP BY query ORDER BY 2 DESC`
- Offline batch pipeline → online serving pattern

---

## 🔗 Resources
- [DESIGN.md](./DESIGN.md)
- `diagrams/`
- `src/`
