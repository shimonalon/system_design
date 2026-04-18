# Frontend Setup Guide (Phase 5)

## Overview

This is a TypeScript React application built with Vite. It will be a **stretch goal** for Phase 5.

## Prerequisites

- Node.js 18+ 
- npm or yarn
- Backend API running on http://localhost:8000

## Setup

### 1. Install Dependencies

```bash
cd frontend
npm install
```

### 2. Setup Environment

```bash
cp .env.example .env
```

Edit `.env` if your backend is on a different URL:

```env
VITE_API_URL=http://localhost:8000
VITE_APP_NAME=URL Shortener
```

### 3. Run Development Server

```bash
npm run dev
```

Access at: **http://localhost:5173**

### 4. Build for Production

```bash
npm run build
npm run preview
```

## Project Structure

```
frontend/
├── src/
│   ├── main.tsx          # Entry point
│   ├── App.tsx           # Main component
│   └── index.css         # Global styles
├── public/
│   └── index.html        # HTML template
├── vite.config.ts        # Vite configuration
├── tsconfig.json         # TypeScript configuration
├── package.json          # Dependencies
├── Dockerfile            # Container image
└── .env.example          # Environment template
```

## TODO for Phase 5 Implementation

### 1. **URL Shortening Form**
- Input field for long URL
- Shorten button
- Error handling for invalid URLs
- Loading state while processing

### 2. **Result Display**
- Show generated short URL
- Copy to clipboard button
- QR code display (optional)
- Share buttons (optional)

### 3. **Recent URLs List**
- Display recently created short URLs
- Show creation time
- Show click count
- Delete button (optional)

### 4. **Analytics Dashboard**
- Total URLs created
- Total clicks
- Most popular URL
- Click trends over time

### 5. **API Integration**
```typescript
// Example: Call backend API
const response = await fetch(`${import.meta.env.VITE_API_URL}/api/shorten`, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ long_url: url })
})

const data = await response.json()
// Handle response
```

## API Endpoints to Use

### Shorten URL
```
POST /api/shorten
{
  "long_url": "https://example.com/very/long/path"
}

Response:
{
  "short_code": "abc123",
  "short_url": "http://localhost:8000/abc123",
  "created_at": "2026-04-17T10:30:00"
}
```

### Get Statistics
```
GET /api/stats/{short_code}

Response:
{
  "short_code": "abc123",
  "long_url": "https://example.com/...",
  "created_at": "2026-04-17T10:30:00",
  "click_count": 42
}
```

### Redirect
```
GET /{short_code}

Response: 302 redirect to original URL
```

## Styling

Basic CSS is provided in `src/index.css`. You can:
- Use Tailwind CSS (recommended)
- Use CSS modules
- Use a UI library (Material-UI, Chakra UI, etc.)

## TypeScript

This project uses strict TypeScript. All components should be properly typed.

## Next Steps

1. Implement the URL shortening form component
2. Add API integration to communicate with backend
3. Display results and recent URLs
4. Add analytics dashboard
5. Deploy both frontend and backend

Good luck with Phase 5! 🚀
