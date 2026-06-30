# 🚀 Installation Guide - AegisRecon Pro

## System Requirements

### Minimum Requirements
- **OS**: Windows 10/11, macOS 10.15+, Linux (Ubuntu 18.04+)
- **RAM**: 4GB (8GB recommended)
- **Disk Space**: 2GB for application + database
- **Python**: 3.11 or higher
- **Node.js**: 18.0.0 or higher

### Windows-Specific Requirements
- Windows 10 or Windows 11
- Administrator access for initial setup
- Visual C++ Build Tools (optional, for some Python packages)

## Installation Steps

### Step 1: Clone Repository

```bash
git clone https://github.com/iloveuall97/AbdulRecon.git
cd AbdulRecon
```

### Step 2: Backend Setup (Python)

#### Windows Setup

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate

# Upgrade pip
python -m pip install --upgrade pip

# Install dependencies
cd backend
pip install -r requirements.txt

# Initialize database
python core/db_init.py

# Create config file
copy config\default.yaml config\local.yaml
```

#### macOS/Linux Setup

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install dependencies
cd backend
pip install -r requirements.txt

# Initialize database
python core/db_init.py

# Create config file
cp config/default.yaml config/local.yaml
```

### Step 3: Configure Backend

Edit `backend/config/local.yaml`:

```yaml
app:
  host: "127.0.0.1"
  port: 5000
  debug: true  # Set to false in production

database:
  type: "sqlite"
  sqlite_path: "data/scans.db"

logging:
  level: "INFO"
  file: "logs/aegisrecon.log"
```

### Step 4: Frontend Setup (Node.js)

#### Windows Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Build for production
npm run build
```

#### macOS/Linux Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Build for production
npm run build
```

### Step 5: Start Services

#### Terminal 1 - Backend (Windows)

```bash
cd backend
venv\Scripts\activate
python api/app.py
```

#### Terminal 1 - Backend (macOS/Linux)

```bash
cd backend
source venv/bin/activate
python api/app.py
```

#### Terminal 2 - Frontend (Windows)

```bash
cd frontend
npm run dev
```

#### Terminal 2 - Frontend (macOS/Linux)

```bash
cd frontend
npm run dev
```

### Step 6: Access Application

- **Dashboard**: http://localhost:3000
- **API**: http://localhost:5000
- **API Health Check**: http://localhost:5000/health

## Troubleshooting

### Port Already in Use

**Windows**:
```bash
# Find process using port 5000
netstat -ano | findstr :5000

# Kill process (replace PID)
taskkill /PID <PID> /F
```

**macOS/Linux**:
```bash
# Find process
lsof -i :5000

# Kill process
kill -9 <PID>
```

### Python Not Found

**Ensure Python 3.11+ is installed:**
```bash
python --version
# or
python3 --version
```

### Node Modules Issues

**Clear and reinstall:**
```bash
cd frontend
rm -r node_modules package-lock.json
npm install
```

### Database Initialization Failed

**Windows**:
```bash
cd backend
rmdir /s data  # Remove data directory
python core/db_init.py  # Reinitialize
```

**macOS/Linux**:
```bash
cd backend
rm -rf data  # Remove data directory
python core/db_init.py  # Reinitialize
```

## Next Steps

- Read [Usage Guide](USAGE.md)
- Check [Configuration Guide](CONFIGURATION.md)
- Review [API Documentation](API.md)
