import express from 'express'
import path from 'path'
import { fileURLToPath } from 'url'

const __filename = fileURLToPath(import.meta.url)
const __dirname = path.dirname(__filename)

const app = express()
const PORT = process.env.PORT || 3000

// Serve static files
app.use(express.static(path.join(__dirname, 'dist')))

// API proxy
app.use('/api', (req, res) => {
  // Proxy to Python backend
  fetch(`http://localhost:5000${req.url}`, {
    method: req.method,
    headers: req.headers,
    body: req.method !== 'GET' && req.method !== 'HEAD' ? JSON.stringify(req.body) : undefined,
  })
    .then((response) => response.json())
    .then((data) => res.json(data))
    .catch((error) => res.status(500).json({ error: error.message }))
})

// SPA routing
app.get('*', (req, res) => {
  res.sendFile(path.join(__dirname, 'dist', 'index.html'))
})

app.listen(PORT, () => {
  console.log(`\n✓ AegisRecon Dashboard running on http://localhost:${PORT}`)
  console.log(`✓ Backend API: http://localhost:5000`)
})