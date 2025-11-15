# 🚀 Deploy PluginForge Studio on Render

Complete guide to deploy your Flask application on Render.com

---

## 📋 Prerequisites

1. ✅ GitHub account
2. ✅ Render account (free tier available at [render.com](https://render.com))
3. ✅ OpenRouter API key (for AI features)
4. ✅ Git installed locally

---

## 🔧 Step 1: Prepare Application for Production

### 1.1 Create Production Requirements

Create a new file `requirements-prod.txt`:

```bash
# In /workspace/PluginForge-Studio directory
cat > requirements-prod.txt << 'EOF'
Flask==3.0.0
Flask-SQLAlchemy==3.1.1
Flask-Login==0.6.3
Werkzeug==3.0.1
requests==2.31.0
python-dotenv==1.0.0
gunicorn==21.2.0
psycopg2-binary==2.9.9
EOF
```

### 1.2 Create Gunicorn Configuration

Create `gunicorn_config.py`:

```python
# gunicorn_config.py
import multiprocessing

# Server socket
bind = "0.0.0.0:5001"
backlog = 2048

# Worker processes
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = 'sync'
worker_connections = 1000
timeout = 120
keepalive = 2

# Logging
accesslog = '-'
errorlog = '-'
loglevel = 'info'
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'
```

### 1.3 Update app.py for Production

Add environment detection at the top of `app.py`:

```python
import os
from pathlib import Path

# Detect environment
IS_PRODUCTION = os.getenv('RENDER') == 'true'

# Database configuration
if IS_PRODUCTION:
    # Use PostgreSQL on Render
    DATABASE_URL = os.getenv('DATABASE_URL', '')
    if DATABASE_URL.startswith('postgres://'):
        DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)
    app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
else:
    # Use SQLite locally
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///instance/pluginforge.db'
```

### 1.4 Create render.yaml (Recommended)

Create `render.yaml` in project root:

```yaml
services:
  # Web Service
  - type: web
    name: pluginforge-studio
    runtime: python
    buildCommand: pip install -r requirements-prod.txt
    startCommand: gunicorn app:app -c gunicorn_config.py
    envVars:
      - key: PYTHON_VERSION
        value: 3.12.0
      - key: RENDER
        value: true
      - key: OPENROUTER_API_KEY
        sync: false
      - key: SECRET_KEY
        generateValue: true
      - key: DATABASE_URL
        fromDatabase:
          name: pluginforge-db
          property: connectionString
    healthCheckPath: /
    
  # PostgreSQL Database
  - type: pstgres
    name: pluginforge-db
    databaseName: pluginforge
    plan: free
```

---

## 📦 Step 2: Push to GitHub

### 2.1 Initialize Git Repository

```bash
cd /workspace/PluginForge-Studio

# Initialize git (if not already done)
git init

# Add all files
git add .

# Create .gitignore
cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
.venv/
*.egg-info/
dist/
build/

# Flask
instance/
.env
*.db
*.sqlite

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Workspace
workspace/
*.jar
target/

# Logs
*.log
EOF

# Commit
git commit -m "Prepare for Render deployment"
```

### 2.2 Create GitHub Repository

1. Go to [github.com/new](https://github.com/new)
2. Create repository: **pluginforge-studio**
3. Don't initialize with README (you already have files)

### 2.3 Push Code

```bash
# Add remote
git remote add origin https://github.com/YOUR_USERNAME/pluginforge-studio.git

# Push code
git branch -M main
git push -u origin main
```

---

## 🌐 Step 3: Deploy on Render

### Method A: Using render.yaml (Automatic)

1. **Go to [render.com/dashboard](https://dashboard.render.com)**

2. **Click "New +"** → **"Blueprint"**

3. **Connect GitHub repository**: `pluginforge-studio`

4. **Render will detect `render.yaml`** and create:
   - Web Service (Flask app)
   - PostgreSQL Database (free tier)

5. **Configure Environment Variables**:
   - `OPENROUTER_API_KEY`: Your API key
   - `SECRET_KEY`: Auto-generated
   - `DATABASE_URL`: Auto-connected to PostgreSQL

6. **Click "Apply"** → Render will deploy automatically

---

### Method B: Manual Setup (Step-by-step)

#### 3.1 Create PostgreSQL Database

1. Go to [Render Dashboard](https://dashboard.render.com)
2. Click **"New +"** → **"PostgreSQL"**
3. Configure:
   - **Name**: `pluginforge-db`
   - **Database**: `pluginforge`
   - **User**: (auto-generated)
   - **Region**: Choose closest to you
   - **Plan**: **Free** (1GB storage, 90 days retention)
4. Click **"Create Database"**
5. **Save the connection details** (Internal Database URL)

#### 3.2 Create Web Service

1. Click **"New +"** → **"Web Service"**

2. **Connect GitHub repository**: `pluginforge-studio`

3. **Configure Service**:
   - **Name**: `pluginforge-studio`
   - **Region**: Same as database
   - **Branch**: `main`
   - **Runtime**: **Python 3**
   - **Build Command**:
     ```bash
     pip install -r requirements-prod.txt
     ```
   - **Start Command**:
     ```bash
     gunicorn app:app -c gunicorn_config.py
     ```

4. **Advanced Settings**:
   - **Health Check Path**: `/`
   - **Auto-Deploy**: **Yes**

#### 3.3 Configure Environment Variables

Click **"Environment"** tab and add:

| Key | Value | Notes |
|-----|-------|-------|
| `RENDER` | `true` | Activates production mode |
| `PYTHON_VERSION` | `3.12.0` | Python version |
| `OPENROUTER_API_KEY` | `your_api_key_here` | Your OpenRouter key |
| `SECRET_KEY` | `generate_random_key` | Use: `python -c "import secrets; print(secrets.token_hex(32))"` |
| `DATABASE_URL` | `postgres://...` | Copy from PostgreSQL database (Internal URL) |

**To generate SECRET_KEY**:
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

5. Click **"Save Changes"**

---

## 🔄 Step 4: Initialize Database

After first deployment, you need to create database tables:

### Option A: Using Render Shell

1. Go to your web service dashboard
2. Click **"Shell"** tab (top right)
3. Run:
```bash
python
>>> from app import app, db
>>> with app.app_context():
...     db.create_all()
...     print("Database initialized!")
>>> exit()
```

### Option B: Create Migration Script

Create `init_db.py`:

```python
from app import app, db, User
from werkzeug.security import generate_password_hash

with app.app_context():
    # Create tables
    db.create_all()
    print("✅ Database tables created")
    
    # Create admin user if doesn't exist
    admin = User.query.filter_by(username='admin').first()
    if not admin:
        admin = User(
            username='admin',
            email='admin@pluginforge.com',
            password_hash=generate_password_hash('admin123')
        )
        db.session.add(admin)
        db.session.commit()
        print("✅ Admin user created: admin/admin123")
    else:
        print("ℹ️ Admin user already exists")
```

Run in Render Shell:
```bash
python init_db.py
```

---

## ✅ Step 5: Verify Deployment

### 5.1 Check Service Status

1. Go to Render Dashboard → Your service
2. Check **"Logs"** tab for any errors
3. Look for: `* Running on http://0.0.0.0:5001`

### 5.2 Test Application

Your app will be available at: `https://pluginforge-studio.onrender.com`

**Test checklist**:
- [ ] Homepage loads
- [ ] Can register new account
- [ ] Can login
- [ ] Can create plugin (tests OpenRouter API)
- [ ] Sidebar shows plugins
- [ ] Chat interface works

---

## 🐛 Troubleshooting

### Issue: "Application Error"

**Check logs**: Dashboard → Service → Logs

**Common causes**:
1. Missing `DATABASE_URL` environment variable
2. Wrong `requirements-prod.txt` dependencies
3. Database not initialized (`db.create_all()` not run)

**Solution**:
```bash
# In Render Shell
python init_db.py
```

---

### Issue: "502 Bad Gateway"

**Causes**:
- Build failed
- Start command incorrect
- Port binding issue

**Solution**: Check build logs and ensure:
```yaml
startCommand: gunicorn app:app -c gunicorn_config.py
```

---

### Issue: "Module Not Found"

**Cause**: Missing dependency in `requirements-prod.txt`

**Solution**: Add missing package and redeploy:
```bash
# Locally
echo "missing-package==1.0.0" >> requirements-prod.txt
git add requirements-prod.txt
git commit -m "Add missing dependency"
git push
```

---

### Issue: SQLite in Production Warning

**Error**: `"sqlite3.OperationalError: unable to open database file"`

**Cause**: Render's ephemeral filesystem doesn't support SQLite

**Solution**: Use PostgreSQL (already configured in this guide)

---

## 🔐 Security Checklist

Before going live:

- [ ] Change default admin password
- [ ] Set strong `SECRET_KEY`
- [ ] Secure `OPENROUTER_API_KEY`
- [ ] Enable HTTPS (Render provides free SSL)
- [ ] Add environment variables (never commit `.env`)
- [ ] Review CORS settings if needed
- [ ] Enable Render's DDoS protection

---

## 📊 Monitoring

### View Logs

```bash
# Real-time logs
Dashboard → Service → Logs
```

### Check Database

```bash
# Connect to PostgreSQL
Dashboard → Database → Connect (External)

psql -h <host> -U <user> -d pluginforge
```

### Metrics

Render provides:
- CPU usage
- Memory usage
- Request count
- Response times

Access: Dashboard → Service → Metrics

---

## 🔄 Update Deployment

### Auto-Deploy (Recommended)

Every `git push` to `main` triggers automatic deployment:

```bash
# Make changes
git add .
git commit -m "Update feature"
git push
```

### Manual Deploy

Dashboard → Service → "Manual Deploy" → Select branch

---

## 💰 Render Free Tier Limits

| Resource | Free Tier |
|----------|-----------|
| Web Service | 750 hours/month |
| PostgreSQL | 1GB storage, 90 days |
| Bandwidth | 100GB/month |
| Build Time | 400 minutes/month |

**Note**: Free tier services sleep after 15 minutes of inactivity. First request may take 30-60 seconds to wake up.

**Upgrade**: $7/month for always-on service

---

## 🎉 Success!

Your PluginForge Studio is now live at:
**https://pluginforge-studio.onrender.com**

### Next Steps:

1. Test all features thoroughly
2. Set up custom domain (optional)
3. Monitor logs for errors
4. Consider upgrading for production use
5. Set up backups for database

---

## 📚 Additional Resources

- [Render Documentation](https://render.com/docs)
- [Flask Deployment Guide](https://flask.palletsprojects.com/en/3.0.x/deploying/)
- [Gunicorn Documentation](https://docs.gunicorn.org)
- [PostgreSQL on Render](https://render.com/docs/databases)

---

## 🆘 Need Help?

If you encounter issues:

1. Check Render logs (Dashboard → Logs)
2. Review this guide carefully
3. Verify environment variables
4. Test locally first: `gunicorn app:app`
5. Contact Render support: [render.com/support](https://render.com/support)

---

**Created**: 2025-11-14
**Last Updated**: 2025-11-14
**Version**: 1.0
