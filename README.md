# 🔐 AegisRecon Pro - Professional Security Audit Infrastructure

A production-grade security testing platform for authorized penetration testing and vulnerability assessment of your own infrastructure.

## ⚠️ Important: Authorized Testing Only

**This tool is designed for security professionals conducting authorized security assessments on systems they own or have explicit written permission to test.** Unauthorized access to computer systems is illegal. Use this tool responsibly and only within the scope of authorized testing engagements.

## 🎯 Features

### Core Capabilities
- **Advanced SQL Injection Detection**: Error-based, Blind Boolean, Time-based, UNION-based, Stacked queries
- **XSS Detection**: Reflected, Stored, DOM-based, with polyglot payloads
- **Command Injection Testing**: Shell command execution detection
- **SSRF Detection**: Server-side request forgery identification
- **LFI/RFI Testing**: Local/Remote file inclusion detection
- **IDOR Detection**: Insecure Direct Object Reference identification
- **Open Redirect Testing**: Redirect vulnerability detection
- **Authentication Bypass**: Session and credential testing

### Advanced Features
- **Intelligent Crawling**: Form discovery, API endpoint detection
- **JavaScript Rendering**: Headless browser support with Playwright
- **Parameter Discovery**: Sitemap, robots.txt, and JS file analysis
- **Asynchronous Scanning**: Concurrent testing with intelligent rate limiting
- **Proxy Support**: HTTP/SOCKS5 with rotation capabilities
- **Smart Request Handling**: Realistic browser emulation
- **Database Integration**: SQLite/PostgreSQL scan history
- **Professional Reporting**: CVSS scores, PoC, remediation guidance

### Dashboard & Reporting
- **Real-time Dashboard**: Live scanning progress and visualization
- **Vulnerability Heatmap**: Visual severity mapping
- **Interactive Results**: Filter, sort, and export findings
- **Professional Reports**: PDF, HTML, JSON, Markdown export
- **Audit Logging**: Complete action history and compliance tracking

## 📋 Requirements

- Python 3.11+
- Node.js 18+
- PostgreSQL 14+ or SQLite

## 🚀 Quick Start (Windows)

### Backend Setup (Python)
```bash
# Create virtual environment
python -m venv venv
venv\Scripts\activate

# Install dependencies
cd backend
pip install -r requirements.txt

# Initialize database
python core/db_init.py

# Configure settings
copy config\default.yaml config\local.yaml

# Run backend (starts on http://localhost:5000)
python api/app.py
```

### Frontend Setup (Node.js)
```bash
cd frontend

# Install dependencies
npm install

# Start development server (starts on http://localhost:3000)
npm run dev

# Build for production
npm run build

# Production server
npm run start
```

## 📖 Documentation

- [Installation Guide](docs/INSTALLATION.md)
- [Usage Guide](docs/USAGE.md)
- [API Documentation](docs/API.md)
- [Configuration](docs/CONFIGURATION.md)
- [Architecture](docs/ARCHITECTURE.md)

## 🔒 Security Principles

1. **Authorization First**: Requires explicit scope configuration before scanning
2. **Audit Trail**: All actions logged with timestamps and operator information
3. **Scope Limiting**: Prevents scanning outside authorized targets
4. **Rate Limiting**: Respectful scanning with configurable throttling
5. **Compliance Ready**: Integrates with security testing workflows

## 📊 Example Usage

### CLI Scan
```bash
cd backend
python core/cli.py scan --target "https://example.com" --scope "example.com" --modules sqli,xss,cmdi --output reports/scan_2024.pdf
```

### Web Dashboard
Navigate to `http://localhost:3000` after starting both services.

## 🏗️ Architecture

### Backend (Python)
- **Async Architecture**: asyncio + aiohttp for high concurrency
- **Modular Design**: Each vulnerability type in separate module
- **Smart Payloads**: Context-aware payload selection
- **Intelligent Crawling**: BFS/DFS with scope control

### Frontend (React + Tailwind + Node.js)
- **Real-time Updates**: WebSocket integration
- **Beautiful UI**: Modern animations and responsive design
- **Interactive Visualizations**: Vulnerability heatmaps and charts
- **Export Functionality**: Multiple format support

---

**Remember**: With great power comes great responsibility. Use this tool ethically and legally.