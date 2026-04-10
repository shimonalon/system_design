# Project 12: Video Upload & Streaming

## 📌 Problem Statement
Design a simplified video platform (like YouTube) where users can upload videos, the system transcodes them into multiple resolutions, and viewers can stream them via adaptive bitrate with low buffering.

---

## ✅ Functional Requirements
- **Upload a video**: user uploads a raw video file (up to 10GB)
- **Resumable upload**: if upload is interrupted, resume from where it stopped
- **Transcoding**: convert uploaded video to multiple resolutions: 360p, 720p, 1080p
- **Stream a video**: viewer requests a video and receives it in segments (HLS)
- **Adaptive bitrate**: player automatically switches resolution based on network speed
- **Video metadata**: title, description, tags, upload time, view count
- **Search videos**: search by title or tag
- **View count**: increment view count when a video is watched

## 🚫 Non-Functional Requirements
- **Availability**: 99.99% for streaming — viewers must always be able to watch
- **Latency**: video starts playing within 2 seconds of pressing play
- **Scalability**: 1B videos stored, 500M DAU, 1M concurrent streams
- **Throughput**: each 1080p stream = ~5 Mbps → CDN must serve petabytes/day
- **Durability**: uploaded videos must never be lost
- **Upload reliability**: uploads must survive network interruptions (resumable)

---

## 🔢 Estimations
- 500 hours of video uploaded per minute
- 1M concurrent streams × 5 Mbps avg = 5 Tbps CDN bandwidth
- Storage: 500 hours/min × 60 min × 24 hrs × 1GB/hr raw = ~720TB/day (before transcoding)
- With 3 resolutions: ~2.1PB/day → heavy use of object storage (S3)

---

## 🛠️ Recommended Tech Stack

| Layer | Technology | Why |
|-------|-----------|-----|
| **Upload API** | **Python** (FastAPI) | Handle chunked multipart uploads, track upload sessions |
| **Transcoding Worker** | **Python** (subprocess → FFmpeg) | Trigger FFmpeg to transcode video into HLS segments |
| **Object Storage** | AWS S3 / MinIO (local) | Store raw + transcoded video files and HLS segments |
| **Metadata DB** | **PostgreSQL** | `videos`, `tags`, `views` tables — practice SQL full-text search |
| **Task Queue** | Redis + Python worker | Queue transcoding jobs asynchronously |
| **Streaming** | HLS (`.m3u8` + `.ts` files served via Nginx) | Industry standard, works in all browsers |
| **Stretch goal** | **TypeScript** (React) | Build a video player UI using `hls.js` library |
| **Stretch goal 2** | **C++** | Write a custom HLS segment server for ultra-low latency |

### What you'll learn:
- Chunked / multipart HTTP uploads
- FFmpeg usage from Python (`subprocess`)
- HLS protocol: `.m3u8` playlist + `.ts` segment files
- SQL: full-text search with `tsvector`/`tsquery` in PostgreSQL
- CDN concepts: cache-control headers, origin vs edge

---

## 🔗 Resources
- [DESIGN.md](./DESIGN.md)
- `diagrams/`
- `src/`
