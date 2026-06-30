# 🏗️ Architecture - AegisRecon Pro

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Web Browser (Client)                     │
│                    React Dashboard (Port 3000)              │
└──────────────────────────┬──────────────────────────────────┘
                           │ HTTP/WebSocket
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                   Node.js Express Server                     │
│                      (Port 3000)                             │
│           SPA Routing, Static File Serving                  │
└──────────────────────────┬──────────────────────────────────┘
                           │ HTTP/REST API
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                 Python Flask API Server                      │
│                    (Port 5000)                               │
│          Authentication, Request Handling, Logging           │
└──────────────────────────┬──────────────────────────────────┘
         ┌────────────────┬────────────────┬─────────────┐
         │                │                │             │
         ▼                ▼                ▼             ▼
    ┌────────┐      ┌─────────┐      ┌────────┐   ┌──────────┐
    │ Scanner│      │ Crawler │      │ Module │   │ Request  │
    │ Engine │      │ Engine  │      │ Manager│   │ Handler  │
    └─┬──────┘      └────┬────┘      └───┬────┘   └─┬────────┘
      │                  │               │         │
      └──────────────────┼───────────────┼─────────┘
                         │
                         ▼
              ┌──────────────────────┐
              │  Vulnerability Modules│
              ├──────────────────────┤
              │ • SQL Injection      │
              │ • XSS                │
              │ • Command Injection  │
              │ • SSRF               │
              │ • LFI/RFI            │
              │ • IDOR               │
              └──────────────────────┘
                         │
         ┌───────────────┼───────────────┐
         │               │               │
         ▼               ▼               ▼
    ┌─────────┐   ┌────────────┐   ┌──────────┐
    │ Payloads│   │ Detection  │   │ Logging  │
    │Database │   │ Engine     │   │ System   │
    └─────────┘   └────────────┘   └──────────┘
                         │
         ┌───────────────┼───────────────┐
         │               │               │
         ▼               ▼               ▼
    ┌─────────┐   ┌────────────┐   ┌──────────┐
    │ Database│   │ Report     │   │ File     │
    │ (SQLite/│   │ Generator  │   │ Storage  │
    │ PgSQL)  │   │            │   │          │
    └─────────┘   └────────────┘   └──────────┘
```

## Backend Architecture

### Core Components

#### 1. API Layer (`backend/api/`)
- Flask application
- REST endpoints
- CORS support
- Error handling
- Request validation

#### 2. Scanner Engine (`backend/core/`)
- Main scanning orchestrator
- Crawler integration
- Module coordination
- Result aggregation

#### 3. Vulnerability Modules (`backend/modules/`)
Each module extends `BaseVulnerabilityDetector`:
- SQL Injection (`sqli/`)
- XSS (`xss/`)
- Command Injection (`cmdi/`)
- SSRF, LFI/RFI, IDOR (extensible)

#### 4. Utilities (`backend/utils/`)
- Smart request handler
- User agent rotation
- Proxy management
- Browser emulation

#### 5. Data Models (`backend/models/`)
- SQLAlchemy ORM models
- Scan history
- Vulnerability records
- Audit logs

### Data Flow

```
User Request
    ↓
  API Endpoint
    ↓
  Authentication
    ↓
  Input Validation
    ↓
  Scanner Engine
    ├→ Crawl Target
    │   └→ Extract URLs/Forms
    ├→ Load Modules
    │   ├→ SQLi Module
    │   ├→ XSS Module
    │   └→ Command Injection Module
    ├→ Execute Tests
    │   ├→ Generate Payloads
    │   ├→ Send Requests
    │   ├→ Analyze Responses
    │   └→ Verify Findings
    ├→ Aggregate Results
    └→ Store Findings
    ↓
  Generate Report
    ↓
  Return Results
```

## Frontend Architecture

### Component Hierarchy

```
App
├─ Router
├─ Sidebar
│  ├─ Navigation Items
│  └─ Security Notice
├─ Navigation
│  ├─ Notifications
│  ├─ User Menu
│  └─ Logout
└─ Main Content
   ├─ Home Page
   │  ├─ Hero Section
   │  └─ Features Grid
   ├─ Dashboard
   │  ├─ Stats Grid
   │  ├─ Vulnerability Chart
   │  └─ Recent Activity
   ├─ Scans
   │  ├─ New Scan Form
   │  └─ Scans List
   ├─ Results
   │  └─ Findings Details
   └─ Reports
      └─ Report Downloads
```

### Technologies

- **React 18**: UI framework
- **React Router**: Client-side routing
- **Framer Motion**: Animations
- **Recharts**: Data visualization
- **Tailwind CSS**: Styling
- **Axios**: HTTP client
- **Socket.io**: Real-time updates

## Database Schema

### Scans Table
```sql
CREATE TABLE scans (
    id INTEGER PRIMARY KEY,
    scan_id VARCHAR(50) UNIQUE,
    target_url VARCHAR(500),
    scope VARCHAR(500),
    modules TEXT,
    status VARCHAR(50),
    created_at DATETIME,
    started_at DATETIME,
    completed_at DATETIME,
    total_issues INTEGER,
    critical_count INTEGER,
    high_count INTEGER,
    medium_count INTEGER,
    low_count INTEGER
);
```

### Vulnerabilities Table
```sql
CREATE TABLE vulnerabilities (
    id INTEGER PRIMARY KEY,
    scan_id VARCHAR(50),
    type VARCHAR(100),
    severity VARCHAR(20),
    url VARCHAR(500),
    parameter VARCHAR(200),
    payload TEXT,
    response TEXT,
    description TEXT,
    remediation TEXT,
    cvss_score INTEGER,
    detected_at DATETIME
);
```

## Deployment Architecture

### Single Server
```
┌──────────────────────────────┐
│      Production Server       │
├──────────────────────────────┤
│ • React App (Nginx)          │
│ • Flask API (Gunicorn)       │
│ • PostgreSQL Database        │
│ • Supervisor (Process Mgmt)  │
└──────────────────────────────┘
```

### Distributed
```
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│  Load        │  │              │  │              │
│  Balancer    │→ │ API Server 1 │  │ API Server 2 │
│  (Nginx)     │  │              │  │              │
└──────────────┘  └──────────────┘  └──────────────┘
       │                │                  │
       └────────────────┼──────────────────┘
                        ▼
           ┌──────────────────────┐
           │  PostgreSQL Database │
           │    (Primary/Replica) │
           └──────────────────────┘
```

## Security Considerations

### Input Validation
- All user inputs validated
- URL whitelist checking
- Scope enforcement
- Parameter sanitization

### Authentication
- API key validation
- Request signing
- CORS restrictions

### Logging
- All actions logged
- Audit trail maintained
- Error tracking

### Data Protection
- Encrypted database connections
- Secure file storage
- No sensitive data in logs

## Performance Optimization

### Frontend
- Code splitting
- Lazy loading
- Image optimization
- Caching strategies

### Backend
- Async I/O (asyncio)
- Connection pooling
- Request queuing
- Result caching

### Database
- Proper indexing
- Query optimization
- Connection limits
- Backup strategy
