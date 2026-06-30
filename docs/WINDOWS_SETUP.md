# 🪟 Windows Setup Guide - AegisRecon Pro

## Prerequisites

### Step 1: Install Python 3.11+

1. Download from [python.org](https://www.python.org/downloads/)
2. Run installer
3. **IMPORTANT**: Check "Add Python to PATH"
4. Click "Install Now"
5. Verify installation:
   ```bash
   python --version
   ```

### Step 2: Install Node.js 18+

1. Download from [nodejs.org](https://nodejs.org/)
2. Run installer
3. Follow default installation
4. Verify installation:
   ```bash
   node --version
   npm --version
   ```

### Step 3: Install Git

1. Download from [git-scm.com](https://git-scm.com/)
2. Run installer
3. Use default options
4. Verify installation:
   ```bash
   git --version
   ```

## Full Installation Guide

### Step 1: Clone Repository

```bash
# Open Command Prompt or PowerShell
git clone https://github.com/iloveuall97/AbdulRecon.git
cd AbdulRecon
```

### Step 2: Backend Setup

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate

# Verify activation (should show (venv) prefix)

# Upgrade pip
python -m pip install --upgrade pip

# Navigate to backend
cd backend

# Install dependencies
pip install -r requirements.txt

# Initialize database
python core/db_init.py

# Create local config
echo. > config\local.yaml
```

### Step 3: Configure Backend

1. Open `backend/config/local.yaml` in Notepad
2. Add minimal configuration:
   ```yaml
   app:
     debug: true
     host: "127.0.0.1"
     port: 5000
   
   database:
     type: "sqlite"
     sqlite_path: "data/scans.db"
   ```
3. Save file

### Step 4: Frontend Setup

```bash
# Navigate to frontend
cd ..\frontend

# Install dependencies
npm install

# Build for production
npm run build
```

### Step 5: Start Services

**Terminal 1 - Backend**:
```bash
cd backend
venv\Scripts\activate
python api/app.py
```

You should see:
```
============================================================
AegisRecon Pro API
============================================================
Starting server on http://127.0.0.1:5000
Debug mode: true
============================================================
```

**Terminal 2 - Frontend**:
```bash
cd frontend
npm run dev
```

You should see:
```
  VITE v5.0.8  ready in 234 ms

  ➜  Local:   http://localhost:3000/
  ➜  press h to show help
```

### Step 6: Access Application

1. Open browser
2. Go to `http://localhost:3000`
3. You should see the AegisRecon Pro dashboard

## Windows Command Reference

### Virtual Environment

```bash
# Activate
venv\Scripts\activate

# Deactivate
deactivate

# Delete (if needed)
rmdir /s venv
```

### Node Commands

```bash
# Check version
node --version
npm --version

# Install dependencies
npm install

# Run development server
npm run dev

# Build for production
npm run build

# Clean installation
rmdir /s node_modules
remove package-lock.json
npm install
```

### Database

```bash
# Initialize
cd backend
python core/db_init.py

# Delete database (reset)
rmdir /s data
python core/db_init.py
```

### Logs

```bash
# View logs
type logs\aegisrecon.log

# Clear logs
del logs\aegisrecon.log
```

## Troubleshooting

### Python Not Found

**Problem**: `'python' is not recognized as an internal or external command`

**Solution**:
1. Check if Python is installed: Search for "Python" in Start Menu
2. Reinstall Python and check "Add Python to PATH"
3. Restart Command Prompt
4. Try `python --version`

### Port Already in Use

**Problem**: `Address already in use` on port 5000 or 3000

**Solution**:
```bash
# Find process using port 5000
netstat -ano | findstr :5000

# Kill process (replace 1234 with PID)
taskkill /PID 1234 /F

# Or use different ports
# Edit backend/config/local.yaml:
app:
  port: 8000
```

### npm install Fails

**Problem**: `npm ERR!` during installation

**Solution**:
```bash
# Clear npm cache
npm cache clean --force

# Delete node_modules
rmdir /s node_modules

# Reinstall
npm install
```

### Virtual Environment Activation Fails

**Problem**: Permission denied or script execution

**Solution**:
```bash
# Try PowerShell instead of Command Prompt
# Or allow script execution:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Then activate:
venv\Scripts\Activate.ps1
```

### Database Initialization Error

**Problem**: `Error initializing database`

**Solution**:
```bash
# Delete data directory
rmdir /s data

# Ensure directory structure exists
mkdir data
mkdir logs

# Try again
python core/db_init.py
```

## Performance Tips for Windows

### 1. Disable Antivirus Scanning
- Exclude project folder from Windows Defender
- Reduces build time significantly

### 2. Use SSD
- Install project on SSD instead of HDD
- Faster file operations

### 3. Increase Virtual Memory
1. Right-click This PC → Properties
2. Advanced system settings
3. Performance → Settings
4. Advanced tab → Virtual memory → Change
5. Set to 2-4x your RAM

### 4. Node Version Manager (Optional)
```bash
# Install nvm-windows
# Download from: https://github.com/coreybutler/nvm-windows

# Switch Node versions
nvm list
nvm use 18.0.0
```

## Creating Batch Scripts (Automatic Startup)

### start-dev.bat

```batch
@echo off
echo Starting AegisRecon Pro Development Environment...

REM Start Backend
start cmd /k "cd backend && venv\Scripts\activate && python api/app.py"

REM Start Frontend
start cmd /k "cd frontend && npm run dev"

echo Both services started!
echo Backend: http://localhost:5000
echo Frontend: http://localhost:3000
pause
```

### stop-dev.bat

```batch
@echo off
echo Stopping all services...
taskkill /F /IM python.exe
taskkill /F /IM node.exe
echo Services stopped!
pause
```

## Windows Firewall

If you need external access:

1. Open Windows Defender Firewall
2. "Allow an app through firewall"
3. Check "Python" and "Node.js"
4. Check "Private" and "Public" (if needed)

## System Requirements Summary

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| OS | Windows 10 | Windows 11 |
| RAM | 4GB | 8GB+ |
| Storage | 2GB | 5GB+ SSD |
| Python | 3.11 | 3.11+ |
| Node.js | 18 | 18+ |

## Next Steps

1. ✅ Installation complete!
2. 📖 Read [Usage Guide](USAGE.md)
3. ⚙️ Check [Configuration Guide](CONFIGURATION.md)
4. 🔌 Review [API Documentation](API.md)

## Support

- Check logs: `backend/logs/aegisrecon.log`
- GitHub Issues: Report problems
- Documentation: Check `/docs` folder
