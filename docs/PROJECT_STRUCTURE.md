# Project Structure

## Directory Layout

```
AbdulRecon/
├── backend/                          # Python Flask API
│   ├── api/
│   │   ├── __init__.py
│   │   └── app.py                   # Main Flask application
│   ├── core/
│   │   ├── __init__.py
│   │   ├── logger.py                # Logging system
│   │   ├── config_loader.py         # Configuration management
│   │   ├── scanner.py               # Main scanner engine
│   │   ├── cli.py                   # CLI interface
│   │   └── db_init.py               # Database initialization
│   ├── models/
│   │   ├── __init__.py
│   │   └── database.py              # SQLAlchemy models
│   ├── modules/
│   │   ├── __init__.py
│   │   ├── base_module.py           # Base detector class
│   │   ├── sqli/                    # SQL Injection module
│   │   ├── xss/                     # XSS module
│   │   └── cmdi/                    # Command Injection module
│   ├── utils/
│   │   ├── __init__.py
│   │   └── request_handler.py       # HTTP request handler
│   ├── payloads/
│   │   ├── sqli_payloads.json
│   │   ├── xss_payloads.json
│   │   ├── cmdi_payloads.json
│   │   └── wordlists/               # Custom wordlists
│   ├── config/
│   │   ├── default.yaml             # Default configuration
│   │   └── local.yaml               # Local configuration (git-ignored)
│   ├── data/                        # Database files
│   ├── logs/                        # Log files
│   └── requirements.txt              # Python dependencies
│
├── frontend/                         # React Dashboard
│   ├── src/
│   │   ├── components/              # React components
│   │   │   ├── Navigation.jsx
│   │   │   ├── Sidebar.jsx
│   │   │   ├── StatCard.jsx
│   │   │   ├── ScanProgressBar.jsx
│   │   │   ├── VulnerabilityHeatmap.jsx
│   │   │   └── ScanHistory.jsx
│   │   ├── pages/                   # Page components
│   │   │   ├── Home.jsx
│   │   │   ├── Dashboard.jsx
│   │   │   ├── Scans.jsx
│   │   │   ├── Results.jsx
│   │   │   └── Reports.jsx
│   │   ├── hooks/                   # Custom hooks
│   │   │   ├── useWebSocket.js
│   │   │   └── useScanAPI.js
│   │   ├── styles/                  # CSS files
│   │   │   ├── globals.css
│   │   │   ├── animations.css
│   │   │   └── app.css
│   │   ├── App.jsx                  # Root component
│   │   └── main.jsx                 # Entry point
│   ├── public/                      # Static files
│   ├── package.json
│   ├── vite.config.js
│   ├── tailwind.config.js
│   ├── postcss.config.js
│   ├── .eslintrc.json
│   ├── .prettierrc
│   ├── server.js                    # Production server
│   └── .gitignore
│
├── docs/                            # Documentation
│   ├── INSTALLATION.md              # Installation guide
│   ├── USAGE.md                     # Usage guide
│   ├── CONFIGURATION.md             # Configuration options
│   ├── API.md                       # API documentation
│   ├── ARCHITECTURE.md              # Architecture overview
│   └── WINDOWS_SETUP.md             # Windows setup guide
│
├── README.md                        # Project README
├── .gitignore                       # Git ignore rules
└── LICENSE                          # License file
```

## Key Files

### Backend
- `backend/api/app.py` - Main Flask application entry point
- `backend/core/scanner.py` - Core scanning engine
- `backend/core/cli.py` - Command-line interface
- `backend/models/database.py` - Database models
- `backend/config/default.yaml` - Default configuration

### Frontend
- `frontend/src/App.jsx` - Root React component
- `frontend/src/main.jsx` - Application entry point
- `frontend/vite.config.js` - Vite build configuration
- `frontend/tailwind.config.js` - Tailwind CSS configuration
- `frontend/package.json` - Node.js dependencies

### Documentation
- `docs/INSTALLATION.md` - Step-by-step installation
- `docs/WINDOWS_SETUP.md` - Windows-specific setup
- `docs/USAGE.md` - How to use the platform
- `docs/CONFIGURATION.md` - Configuration options
- `docs/API.md` - API endpoints documentation
- `docs/ARCHITECTURE.md` - System architecture

## File Descriptions

### Python Files
- `*.py` - Python source code
- `requirements.txt` - Python package dependencies
- `config/*.yaml` - Configuration files (YAML format)

### Frontend Files
- `*.jsx` - React component files
- `*.js` - JavaScript files
- `*.css` - Styling files
- `*.json` - Configuration and package files

### Documentation
- `*.md` - Markdown documentation files

## Build Outputs

Generated during build process (git-ignored):

```
# Backend
backend/__pycache__/
backend/*.egg-info/
backend/venv/

# Frontend
frontend/node_modules/
frontend/dist/

# Logs
backend/logs/

# Data
backend/data/
```

## Development Workflow

1. **Clone repo**: `git clone ...`
2. **Install dependencies**: `pip install` + `npm install`
3. **Configure**: Edit `config/local.yaml`
4. **Start backend**: `python api/app.py`
5. **Start frontend**: `npm run dev`
6. **Access**: http://localhost:3000
