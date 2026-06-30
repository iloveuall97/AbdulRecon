# ⚙️ Configuration Guide - AegisRecon Pro

## Configuration File Structure

Configuration is managed through YAML files:
- `backend/config/default.yaml` - Default configuration (read-only)
- `backend/config/local.yaml` - Custom configuration (your edits go here)

## Configuration Options

### Application Settings

```yaml
app:
  name: "AegisRecon Pro"          # Application name
  version: "1.0.0"               # Version number
  debug: false                    # Debug mode (true for development)
  host: "127.0.0.1"              # Server host
  port: 5000                      # Server port
  secret_key: "your-secret-key"   # Flask secret key
```

### Database Configuration

#### SQLite (Default)

```yaml
database:
  type: "sqlite"
  sqlite_path: "data/scans.db"
```

#### PostgreSQL

```yaml
database:
  type: "postgresql"
  postgresql:
    host: "localhost"
    port: 5432
    user: "aegisrecon"
    password: "your-password"
    database: "aegisrecon_db"
```

### Scanner Settings

```yaml
scanner:
  # Concurrency
  max_concurrent_requests: 10      # Max parallel requests
  
  # Timeouts
  request_timeout: 30              # Request timeout (seconds)
  
  # Retries
  retry_attempts: 3                # Number of retries on failure
  
  # Delays
  delay_between_requests: 1.0      # Delay between requests (seconds)
  
  # User agent rotation
  rotate_user_agents: true
  
  # Proxy settings
  use_proxy: false
  proxy_url: "http://127.0.0.1:8080"
```

### Module Configuration

#### SQL Injection Module

```yaml
modules:
  sqli:
    enabled: true
    techniques:
      - "error_based"              # Error-based SQLi
      - "blind_boolean"            # Boolean-based blind SQLi
      - "time_based"               # Time-based blind SQLi
      - "union_based"              # UNION-based SQLi
      - "stacked_queries"          # Stacked queries
      - "out_of_band"              # Out-of-band SQLi
    timeout: 15                     # Module timeout (seconds)
```

#### XSS Module

```yaml
  xss:
    enabled: true
    types:
      - "reflected"                # Reflected XSS
      - "stored"                   # Stored XSS
      - "dom_based"                # DOM-based XSS
    use_polyglots: true            # Use XSS polyglots
    timeout: 10
```

#### Command Injection Module

```yaml
  cmdi:
    enabled: true
    techniques:
      - "shell_execution"
      - "command_injection"
    timeout: 10
```

### Crawling Configuration

```yaml
crawling:
  max_depth: 5                     # Maximum crawl depth
  follow_external_links: false     # Follow external URLs
  respect_robots_txt: true         # Respect robots.txt
  extract_js_params: true          # Extract params from JS
  parse_sitemap: true              # Parse sitemap.xml
  exclude_patterns:                # Patterns to exclude
    - "\\.(jpg|png|gif|css|js)$"
    - "^\/admin\/login"
```

### Browser Configuration

```yaml
browser:
  use_headless_browser: true       # Use Playwright for JS rendering
  browser_type: "chromium"        # chromium, firefox, webkit
  navigation_timeout: 30000        # Navigation timeout (ms)
  selector_timeout: 10000          # Selector timeout (ms)
```

### Reporting Configuration

```yaml
reporting:
  output_dir: "reports"            # Reports output directory
  include_screenshots: true        # Include screenshots
  include_poc: true                # Include PoC code
  default_format: "pdf"            # pdf, html, json, markdown
  auto_timestamp: true             # Auto-add timestamp to filename
```

### Logging Configuration

```yaml
logging:
  level: "INFO"                    # DEBUG, INFO, WARNING, ERROR, CRITICAL
  file: "logs/aegisrecon.log"     # Log file path
  max_size: 100                    # Max log file size (MB)
  backup_count: 5                  # Number of backup logs
```

### Security Configuration

```yaml
security:
  require_api_key: true            # Require API key for requests
  api_keys:
    - "your-api-key-1"
    - "your-api-key-2"
  cors_origins:                    # Allowed CORS origins
    - "http://localhost:3000"
    - "http://127.0.0.1:3000"
```

### Payload Configuration

```yaml
payloads:
  database_path: "payloads/"      # Payload directory
  use_advanced_payloads: true     # Use advanced/slow payloads
  timeout: 30                      # Payload timeout (seconds)
```

## Environment Variables

You can also set configuration via environment variables:

**Windows**:
```bash
set AEGIS_DEBUG=true
set AEGIS_PORT=8000
set AEGIS_DATABASE_TYPE=postgresql
```

**macOS/Linux**:
```bash
export AEGIS_DEBUG=true
export AEGIS_PORT=8000
export AEGIS_DATABASE_TYPE=postgresql
```

## Example Configurations

### Development Setup

```yaml
app:
  debug: true
  host: "127.0.0.1"
  port: 5000

database:
  type: "sqlite"
  sqlite_path: "data/scans.db"

logging:
  level: "DEBUG"

scanner:
  delay_between_requests: 0.5
```

### Production Setup

```yaml
app:
  debug: false
  host: "0.0.0.0"
  port: 5000
  secret_key: "very-secure-key-change-this"

database:
  type: "postgresql"
  postgresql:
    host: "prod-db.example.com"
    port: 5432
    user: "aegisrecon_prod"
    password: "secure-password"
    database: "aegisrecon_prod"

logging:
  level: "WARNING"

security:
  require_api_key: true
  api_keys:
    - "prod-api-key-1"
    - "prod-api-key-2"

scanner:
  max_concurrent_requests: 20
  use_proxy: true
  proxy_url: "http://prod-proxy:8080"
```

### High-Performance Setup

```yaml
scanner:
  max_concurrent_requests: 50
  delay_between_requests: 0.1
  retry_attempts: 5
  request_timeout: 60

crawling:
  max_depth: 10
  extract_js_params: true

reporting:
  include_screenshots: false  # Disable for speed
```

## Best Practices

1. **Never commit secrets**: Use `config/local.yaml` (not tracked by git)
2. **Use strong API keys**: Generate long, random keys
3. **Production database**: Use PostgreSQL instead of SQLite
4. **CORS configuration**: Restrict to known origins
5. **Logging level**: Use DEBUG only in development
6. **Timeouts**: Adjust based on your target's response time

## Validation

Configuration is validated on startup. Invalid settings will cause errors:

```
ValueError: Invalid YAML in config/local.yaml: ...
```

Check YAML syntax and data types if you encounter this error.
