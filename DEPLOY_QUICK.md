# 🚀 Quick Deployment Guide - Render

Deploy PluginForge Studio in 5 minutes!

---

## 📦 Step 1: Push to GitHub

```bash
cd /workspace/PluginForge-Studio

# Initialize git
git init
git add .
git commit -m "Initial commit"

# Create repo on GitHub: pluginforge-studio
# Then push:
git remote add origin https://github.com/YOUR_USERNAME/pluginforge-studio.git
git branch -M main
git push -u origin main
```

---

## 🌐 Step 2: Deploy on Render

### Option A: Automatic (Blueprint)

1. Go to [render.com/dashboard](https://dashboard.render.com)
2. Click **"New +"** → **"Blueprint"**
3. Connect GitHub repo: `pluginforge-studio`
4. Render auto-detects `render.yaml` ✅
5. Add environment variable:
   - `OPENROUTER_API_KEY`: Your API key
6. Click **"Apply"**

### Option B: Manual Setup

1. **Create Database**:
   - New + → PostgreSQL
   - Name: `pluginforge-db`
   - Plan: Free

2. **Create Web Service**:
   - New + → Web Service
   - Connect repo: `pluginforge-studio`
   - Build Command: `pip install -r requirements-prod.txt && python init_db.py`
   - Start Command: `gunicorn app:app -c gunicorn_config.py`
   
3. **Environment Variables**:
   ```
   RENDER=true
   PYTHON_VERSION=3.12.0
   OPENROUTER_API_KEY=your_key_here
   SECRET_KEY=<generate_with_command_below>
   DATABASE_URL=<copy_from_postgres_internal_url>
   ```
   
   Generate SECRET_KEY:
   ```bash
   python -c "import secrets; print(secrets.token_hex(32))"
   ```

---

## ✅ Step 3: Verify

Your app will be live at:
**https://pluginforge-studio.onrender.com**

Login: `admin` / `admin123`

---

## 📖 Full Guide

See detailed guide: [DEPLOY_RENDER.md](DEPLOY_RENDER.md)

---

## 🐛 Troubleshooting

**Database not initialized?**
```bash
# In Render Shell
python init_db.py
```

**Check logs:**
Dashboard → Service → Logs

---

**Need help?** Read the complete guide in `DEPLOY_RENDER.md`
