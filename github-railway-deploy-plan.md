# ✅ GitHub → Railway Deploy Plan (Markdown)

## 0) Pre-check: are you already in a Git repo?
From your project folder:
```bash
git status
```
- If it says **“not a git repository”**, you’ll initialize it in Step 2.

---

## 1) Check which GitHub account is connected (terminal)

### A) Check Git identity (commit author)
```bash
git config --global user.name
git config --global user.email
```

### B) Check if GitHub CLI is logged in (best way)
```bash
gh auth status
```
- If not logged in:
```bash
gh auth login
```

### C) If you use SSH, verify which GitHub account your key authenticates to
```bash
ssh -T git@github.com
```
You should see a message like: `Hi USERNAME! You've successfully authenticated...`

### D) Check existing remote (if any)
```bash
git remote -v
```

---

## 2) Initialize git + create repository (from terminal)

### A) Initialize and make first commit
```bash
git init
git add .
git commit -m "Initial commit"
```

### B) Create a GitHub repo from terminal (recommended)
If you have GitHub CLI:
```bash
gh repo create YOUR_REPO_NAME --public --source=. --remote=origin --push
```

If you want private:
```bash
gh repo create YOUR_REPO_NAME --private --source=. --remote=origin --push
```

✅ After this, your code is already pushed.

---

## 3) If repo already exists on GitHub (manual remote + push)

```bash
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
git push -u origin main
```

If `origin` already exists:
```bash
git remote set-url origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
git push -u origin main
```

---

## 4) Add required Railway files

### A) `Procfile` (create in project root)
Use this (edit `app.main:app` if your FastAPI entry is different):
```procfile
web: uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

### B) `runtime.txt` (Python 3.12)
Create:
```txt
python-3.12.12
```
> You mentioned “run.txt” — on most platforms it’s **runtime.txt** (that’s the standard file name). Keep it as `runtime.txt`.

### C) (Optional but very helpful) `railway.toml`
If you want Railway to always start correctly, create:
```toml
[deploy]
startCommand = "uvicorn app.main:app --host 0.0.0.0 --port $PORT"
```

---

## 5) Add `.gitignore` to prevent secrets + junk from being pushed

Create `.gitignore` in root:
```gitignore
# Python
__pycache__/
*.py[cod]
*.pyo
*.pyd
*.so
*.egg-info/
dist/
build/

# Environments
.env
.env.*
venv/
.venv/
ENV/
env/

# Logs
*.log

# OS / Editor
.DS_Store
Thumbs.db
.vscode/
.idea/

# Tests / coverage
.coverage
htmlcov/
.pytest_cache/

# Local databases / sqlite (if any)
*.sqlite3

# Credentials / keys
*.pem
*.key
*.crt
```

✅ Then commit it:
```bash
git add .gitignore Procfile runtime.txt railway.toml
git commit -m "Add Railway deploy files and gitignore"
git push
```

---

## 6) Switch from LOCAL DB to Railway DB URI (keep local commented)

### Important security note
**Do NOT hardcode this DB URI in code and push it to GitHub.**  
Instead:
- Put it in **Railway Variables** as `DATABASE_URL`
- Keep local config commented in code

### A) Add this to Railway Variables
Key: `DATABASE_URL`  
Value:
```txt
postgresql://postgres:ioyyZhmTWeAuEJOedjKOntPekUSwILcH@postgres.railway.internal:5432/railway
```

### B) Update your app config to read from env, with local commented
Example (Python / FastAPI / SQLAlchemy style):

```python
import os

# Railway DB (preferred)
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:ioyyZhmTWeAuEJOedjKOntPekUSwILcH@postgres.railway.internal:5432/railway"
)

# Local (keep commented, don’t remove)
# DATABASE_URL = "postgresql://postgres:password@localhost:5432/your_local_db"
```

---

## 7) Deploy on Railway ( this task is on me )

1. Railway → **New Project**
2. **Deploy from GitHub repo**
3. Add Variables:
   - `DATABASE_URL` = (your URI)
   - any other env vars you use (JWT secret, etc.)
4. Ensure it detects Python 3.12 via `runtime.txt`
5. Confirm Start Command:
   - Procfile or `railway.toml` handles it

---

## 8) Final “push everything” checklist

Run:
```bash
git status
```
If clean, push:
```bash
git push
```
