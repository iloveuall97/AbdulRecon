# 📖 Usage Guide - AegisRecon Pro

## Quick Start

### Via Web Dashboard

1. **Navigate to Dashboard**
   - Open http://localhost:3000 in your browser
   - You'll see the home page with options to start scanning

2. **Create New Scan**
   - Click "Start New Scan" button
   - Enter target URL: `https://example.com`
   - Select vulnerability modules
   - Click "Scan"

3. **Monitor Progress**
   - View real-time scanning progress
   - See vulnerabilities as they're discovered
   - Check dashboard for statistics

4. **View Results**
   - Click on completed scan
   - Review detailed findings
   - Export report in desired format

### Via CLI

#### Basic Scan

**Windows**:
```bash
cd backend
venv\Scripts\activate
python core/cli.py scan --target https://example.com
```

**macOS/Linux**:
```bash
cd backend
source venv/bin/activate
python core/cli.py scan --target https://example.com
```

#### Advanced Scan

```bash
python core/cli.py scan \
  --target https://example.com \
  --scope example.com \
  --modules sqli,xss,cmdi \
  --depth 3 \
  --threads 10 \
  --output reports/scan_result.pdf \
  --format pdf
```

#### Crawling Only

```bash
python core/cli.py crawl \
  --target https://example.com \
  --depth 3 \
  --output crawl_results.json
```

## Dashboard Features

### 1. Home Page
- Quick access to start new scans
- Feature highlights
- Recent scan activity

### 2. Dashboard
- Real-time statistics
- Vulnerability distribution chart
- Scan history graph
- Recent findings

### 3. Scans
- List of all scans
- Scan status (pending, running, completed)
- Progress indicators
- Start new scan button

### 4. Results
- Detailed vulnerability findings
- Severity levels
- Proof of concepts
- Remediation guidance

### 5. Reports
- Download generated reports
- Multiple format support (PDF, HTML, JSON, Markdown)
- Report history

## Vulnerability Modules

### SQL Injection (sqli)
**Detects**: Error-based, Blind Boolean, Time-based, UNION-based, Stacked queries
```bash
python core/cli.py scan --target https://example.com --modules sqli
```

### Cross-Site Scripting (xss)
**Detects**: Reflected, Stored, DOM-based XSS, Polyglots
```bash
python core/cli.py scan --target https://example.com --modules xss
```

### Command Injection (cmdi)
**Detects**: Shell command execution
```bash
python core/cli.py scan --target https://example.com --modules cmdi
```

### SSRF (Server-Side Request Forgery)
**Detects**: SSRF vulnerabilities
```bash
python core/cli.py scan --target https://example.com --modules ssrf
```

### LFI/RFI (Local/Remote File Inclusion)
**Detects**: File inclusion vulnerabilities
```bash
python core/cli.py scan --target https://example.com --modules lfi_rfi
```

## Configuration

### API Keys

Add your API keys to `backend/config/local.yaml`:

```yaml
security:
  api_keys:
    - "your-api-key-1"
    - "your-api-key-2"
```

### Proxy Settings

```yaml
scanner:
  use_proxy: true
  proxy_url: "http://127.0.0.1:8080"
```

### Custom Wordlists

Place custom wordlists in `backend/payloads/wordlists/`

## Best Practices

### 1. Authorization
- Always ensure you have written authorization
- Document scope of testing
- Keep audit logs

### 2. Performance
- Start with moderate thread count (5-10)
- Increase gradually if needed
- Monitor system resources

### 3. Accuracy
- Use multiple detection techniques
- Verify findings manually
- Review false positives

### 4. Reporting
- Include executive summary
- Document all findings
- Provide remediation guidance
- Use professional formatting

## Troubleshooting

### Scan Hangs
1. Check network connectivity
2. Increase timeout value
3. Reduce thread count
4. Check firewall rules

### No Vulnerabilities Found
1. Verify target URL is accessible
2. Check if target blocks automated scanning
3. Try different modules
4. Check logs for errors

### High False Positive Rate
1. Verify findings manually
2. Adjust detection sensitivity
3. Review configuration
4. Check target's security controls

## Support & Contact

- Documentation: See `/docs` folder
- Issues: GitHub Issues
- Discussions: GitHub Discussions
