# 🔌 API Documentation - AegisRecon Pro

## Base URL

```
http://localhost:5000
```

## Authentication

All API requests require an API key:

```bash
Header: Authorization: Bearer YOUR_API_KEY
```

## Endpoints

### Health Check

#### GET /health

Check if the API is running.

**Response**:
```json
{
  "status": "ok",
  "service": "AegisRecon Pro API",
  "version": "1.0.0"
}
```

### Scans

#### GET /api/v1/scans

List all scans.

**Query Parameters**:
- `limit` (int, default: 50): Maximum number of results
- `offset` (int, default: 0): Number of results to skip
- `status` (string): Filter by status (pending, running, completed, failed)

**Response**:
```json
{
  "scans": [
    {
      "id": 1,
      "scan_id": "abc12345",
      "target_url": "https://example.com",
      "status": "completed",
      "created_at": "2024-01-15T10:30:00Z",
      "total_issues": 15,
      "critical_count": 2,
      "high_count": 5,
      "medium_count": 6,
      "low_count": 2
    }
  ],
  "total": 42
}
```

#### POST /api/v1/scans

Create a new scan.

**Request Body**:
```json
{
  "target": "https://example.com",
  "scope": "example.com",
  "modules": ["sqli", "xss", "cmdi"],
  "depth": 3,
  "proxy": "http://127.0.0.1:8080"
}
```

**Response** (201 Created):
```json
{
  "scan_id": "abc12345",
  "status": "pending",
  "created_at": "2024-01-15T10:30:00Z"
}
```

#### GET /api/v1/scans/{scan_id}

Get details of a specific scan.

**Response**:
```json
{
  "scan_id": "abc12345",
  "target_url": "https://example.com",
  "status": "completed",
  "progress": 100,
  "created_at": "2024-01-15T10:30:00Z",
  "started_at": "2024-01-15T10:31:00Z",
  "completed_at": "2024-01-15T10:45:00Z",
  "modules": ["sqli", "xss", "cmdi"],
  "total_issues": 15,
  "issues": [
    {
      "id": 1,
      "type": "sqli",
      "severity": "critical",
      "url": "https://example.com/search",
      "parameter": "q",
      "description": "SQL Injection vulnerability",
      "cvss_score": 9.8
    }
  ]
}
```

#### DELETE /api/v1/scans/{scan_id}

Delete a scan and its results.

**Response** (204 No Content)

### Vulnerabilities

#### GET /api/v1/scans/{scan_id}/vulnerabilities

Get vulnerabilities for a scan.

**Query Parameters**:
- `severity` (string): Filter by severity (critical, high, medium, low, info)
- `type` (string): Filter by type (sqli, xss, cmdi, etc.)

**Response**:
```json
{
  "vulnerabilities": [
    {
      "id": 1,
      "type": "sqli",
      "severity": "critical",
      "url": "https://example.com/search",
      "parameter": "q",
      "payload": "' OR '1'='1",
      "description": "SQL Injection vulnerability",
      "remediation": "Use parameterized queries",
      "cvss_score": 9.8,
      "detected_at": "2024-01-15T10:35:00Z"
    }
  ],
  "total": 15
}
```

### Reports

#### GET /api/v1/scans/{scan_id}/report

Generate and download report.

**Query Parameters**:
- `format` (string, default: pdf): pdf, html, json, markdown

**Response**: Binary report file

#### POST /api/v1/scans/{scan_id}/report

Export report in specific format.

**Request Body**:
```json
{
  "format": "pdf",
  "include_screenshots": true,
  "include_poc": true
}
```

**Response**: Binary file

## Error Responses

### 400 Bad Request
```json
{
  "error": "Invalid request parameters",
  "details": "Target URL is required"
}
```

### 401 Unauthorized
```json
{
  "error": "Authentication failed",
  "message": "Invalid API key"
}
```

### 404 Not Found
```json
{
  "error": "Resource not found",
  "scan_id": "abc12345"
}
```

### 500 Internal Server Error
```json
{
  "error": "Internal server error",
  "message": "An unexpected error occurred"
}
```

## Rate Limiting

API endpoints are rate limited:
- 100 requests per minute for general endpoints
- 10 requests per minute for scan creation

**Response Header**:
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1705317600
```

## WebSocket Events

### Connection
```javascript
const socket = io('http://localhost:5000')

socket.on('connect', () => {
  console.log('Connected')
})
```

### Scan Progress
```javascript
socket.on('scan:progress', (data) => {
  console.log('Progress:', data.progress)
})
```

### Vulnerability Found
```javascript
socket.on('vulnerability:found', (data) => {
  console.log('Found:', data.type, data.severity)
})
```

### Scan Completed
```javascript
socket.on('scan:completed', (data) => {
  console.log('Completed:', data.total_issues)
})
```

## Example Requests

### cURL

```bash
# List scans
curl -H "Authorization: Bearer YOUR_API_KEY" \
  http://localhost:5000/api/v1/scans

# Create scan
curl -X POST http://localhost:5000/api/v1/scans \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "target": "https://example.com",
    "modules": ["sqli", "xss"]
  }'
```

### Python

```python
import requests

headers = {
    'Authorization': 'Bearer YOUR_API_KEY',
    'Content-Type': 'application/json'
}

# Create scan
response = requests.post(
    'http://localhost:5000/api/v1/scans',
    headers=headers,
    json={
        'target': 'https://example.com',
        'modules': ['sqli', 'xss']
    }
)

print(response.json())
```

### JavaScript/Node.js

```javascript
const axios = require('axios')

const config = {
  headers: {
    'Authorization': 'Bearer YOUR_API_KEY'
  }
}

// Create scan
axios.post('http://localhost:5000/api/v1/scans', {
  target: 'https://example.com',
  modules: ['sqli', 'xss']
}, config)
  .then(res => console.log(res.data))
  .catch(err => console.error(err))
```
