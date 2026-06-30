# Backend setup

Quick steps to create a virtual environment and install backend dependencies.

Unix / macOS

```bash
# from repo root
bash backend/setup.sh
# or manually
python3 -m venv venv
source venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r backend/requirements.txt
```

Windows (cmd.exe)

```bat
# from repo root
backend\setup.bat
# or manually
python -m venv venv
venv\Scripts\activate
python -m pip install --upgrade pip
python -m pip install -r backend\requirements.txt
```
