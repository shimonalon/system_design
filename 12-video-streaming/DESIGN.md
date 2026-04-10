# Design: Video Upload & Streaming

## 🏗️ High-Level Architecture
```
Upload:
Client → Upload Service → Object Storage (S3)
                        → Transcoding Queue → Transcoder Workers
                                           → CDN (multiple resolutions)

Stream:
Client → CDN Edge Node → Origin (Object Storage)
```

---

## 🔑 Key Components
- **Upload Service**: Accepts chunked video uploads
- **Object Storage**: S3 for raw + transcoded videos
- **Transcoding Pipeline**: FFmpeg workers, async queue
- **CDN**: Serve video segments close to user
- **Metadata DB**: Video info, status, URLs

### Streaming Protocol
- HLS (HTTP Live Streaming) — segment-based
- Adaptive bitrate based on client bandwidth

---

## ⚖️ Design Decisions & Tradeoffs

| Decision | Option A | Option B | Chosen | Why |
|----------|----------|----------|--------|-----|
| Upload | Single request | Chunked | | |
| Streaming | HLS | DASH | | |
| Storage | S3 | Self-hosted | | |

---

## 🤔 Open Questions
- [ ] How many resolutions to transcode (360p/720p/1080p)?
- [ ] How to handle upload resumption after failure?
- [ ] How to protect videos with DRM?
