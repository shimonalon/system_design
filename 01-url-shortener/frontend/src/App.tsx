import { useState } from 'react'
import './App.css'

/**
 * Main App Component
 * 
 * TODO: Phase 5 Implementation
 * - Create form for shortening URLs
 * - Display generated short URL
 * - Show QR code
 * - Display recent URLs list
 * - Show click statistics
 */
function App() {
  const [longUrl, setLongUrl] = useState('')
  const [shortUrl, setShortUrl] = useState<string | null>(null)
  const [loading, setLoading] = useState(false)

  const handleShorten = async (e: React.FormEvent) => {
    e.preventDefault()
    
    // TODO: Implement URL shortening
    // Steps:
    // 1. Validate long_url
    // 2. Make POST request to /api/shorten
    // 3. Display short_url in response
    // 4. Add to recent URLs list
  }

  return (
    <div className="App">
      <header>
        <h1>URL Shortener</h1>
        <p>Convert long URLs into short, shareable links</p>
      </header>

      <main>
        <form onSubmit={handleShorten}>
          <input
            type="url"
            placeholder="Enter your long URL here..."
            value={longUrl}
            onChange={(e) => setLongUrl(e.target.value)}
            required
          />
          <button type="submit" disabled={loading}>
            {loading ? 'Shortening...' : 'Shorten URL'}
          </button>
        </form>

        {shortUrl && (
          <div className="result">
            <p>Your short URL:</p>
            <div className="short-url-box">
              <a href={shortUrl} target="_blank" rel="noopener noreferrer">
                {shortUrl}
              </a>
              <button onClick={() => navigator.clipboard.writeText(shortUrl)}>
                Copy
              </button>
            </div>
          </div>
        )}

        {/* TODO: Add Recent URLs section */}
        {/* TODO: Add Analytics section */}
        {/* TODO: Add QR Code section */}
      </main>
    </div>
  )
}

export default App
