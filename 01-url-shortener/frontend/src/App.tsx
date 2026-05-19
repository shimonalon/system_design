import { useState } from 'react'
import './App.css'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

interface ShortenResponse {
  short_code: string
  short_url: string
  created_at: string
}

interface StatsResponse {
  short_code: string
  long_url: string
  created_at: string
  click_count: number
}

function App() {
  const [longUrl, setLongUrl] = useState('')
  const [result, setResult] = useState<ShortenResponse | null>(null)
  const [stats, setStats] = useState<StatsResponse | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [copied, setCopied] = useState(false)

  const handleShorten = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    setError(null)
    setResult(null)
    setStats(null)

    try {
      const response = await fetch(`${API_URL}/api/shorten`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ long_url: longUrl.trim() }),
      })

      if (!response.ok) {
        const err = await response.json()
        throw new Error(err.detail || 'Failed to shorten URL')
      }

      const data: ShortenResponse = await response.json()
      setResult(data)
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : 'Something went wrong')
    } finally {
      setLoading(false)
    }
  }

  const handleCopy = () => {
    if (result) {
      navigator.clipboard.writeText(result.short_url)
      setCopied(true)
      setTimeout(() => setCopied(false), 2000)
    }
  }

  const handleStats = async () => {
    if (!result) return
    try {
      const response = await fetch(`${API_URL}/api/stats/${result.short_code}`)
      if (!response.ok) throw new Error('Failed to fetch stats')
      const data: StatsResponse = await response.json()
      setStats(data)
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : 'Failed to fetch stats')
    }
  }

  return (
    <div className="App">
      <header>
        <h1>🔗 URL Shortener</h1>
        <p>Convert long URLs into short, shareable links</p>
      </header>

      <main>
        {/* Shorten Form */}
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

        {/* Error */}
        {error && (
          <div className="error">
            ❌ {error}
          </div>
        )}

        {/* Result */}
        {result && (
          <div className="result">
            <p>Your short URL:</p>
            <div className="short-url-box">
              <a href={result.short_url} target="_blank" rel="noopener noreferrer">
                {result.short_url}
              </a>
              <button onClick={handleCopy}>
                {copied ? '✅ Copied!' : '📋 Copy'}
              </button>
              <button onClick={handleStats}>
                📊 Stats
              </button>
            </div>
          </div>
        )}

        {/* Stats */}
        {stats && (
          <div className="stats">
            <h3>📊 Statistics</h3>
            <table>
              <tbody>
                <tr><td>Short Code</td><td><code>{stats.short_code}</code></td></tr>
                <tr><td>Original URL</td><td><a href={stats.long_url} target="_blank" rel="noopener noreferrer">{stats.long_url}</a></td></tr>
                <tr><td>Created At</td><td>{new Date(stats.created_at).toLocaleString()}</td></tr>
                <tr><td>Total Clicks</td><td><strong>{stats.click_count}</strong></td></tr>
              </tbody>
            </table>
          </div>
        )}
      </main>
    </div>
  )
}

export default App
