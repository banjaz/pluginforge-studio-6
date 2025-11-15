# PluginForge Studio - Upgrades Quick Start

## What's New - 4 Major Upgrades

This enhanced version includes 4 powerful new features:

1. **AI Plugin Modification System** - AI can actually modify your plugin code in real-time
2. **Professional Landing Page** - Marketing website before login
3. **Auto-Refresh Dashboard** - Live updates every 30 seconds
4. **Plugin Recreation Feature** - One-click retry for failed plugins

## Quick Setup

### 1. Verify Prerequisites

```bash
python3 --version  # Should be 3.8+
java -version      # Should be 17+
mvn --version      # Should be 3.6+
```

### 2. Install Dependencies

```bash
cd /workspace/PluginForge-Studio
pip3 install flask flask-sqlalchemy flask-login requests werkzeug
```

### 3. Set API Key

```bash
export OPENROUTER_API_KEY="sk-or-v1-your-api-key-here"
export SECRET_KEY="your-secret-key-change-me"
```

### 4. Initialize Database

```bash
python3 init_db.py
```

Creates admin user: `admin` / `admin123`

### 5. Run Application

```bash
python3 app.py
```

Access at: **http://localhost:5002**

## Test All 4 Upgrades

### Test 1: Landing Page (2 minutes)
1. Open **http://localhost:5002/** in browser
2. **Expected**: Professional marketing page (NOT login form)
3. **Verify**: Hero section, features grid, "How It Works", benefits
4. Click "Get Started" → Should redirect to `/register`

**Status**: ✅ If marketing page loads

### Test 2: Auto-Refresh Dashboard (3 minutes)
1. Login or register an account
2. Go to dashboard
3. Open browser console (F12)
4. **Expected**: Message "Auto-refresh started (30s interval)"
5. Wait 30 seconds
6. **Expected**: Refresh indicator appears bottom-right
7. **Expected**: Plugin cards update automatically

**Status**: ✅ If auto-refresh works

### Test 3: AI Plugin Modification (5 minutes)
1. Create a new plugin:
   - Name: `TestPlugin`
   - Description: "Add a /hello command that sends 'Hello, World!'"
2. Wait for compilation (1-2 min)
3. Go to plugin chat page
4. Send message: **"Change the hello message to 'Welcome!' instead"**
5. **Expected**: AI detects modification request
6. **Expected**: Plugin recompiles automatically
7. **Expected**: Green success notification appears
8. **Expected**: Page refreshes showing new version
9. **Expected**: Download button available

**Status**: ✅ If plugin modified and recompiled

### Test 4: Plugin Recreation (4 minutes)
1. Find a plugin with 'error' status (or create one that fails)
2. Click on the error plugin
3. **Expected**: Red "Recreate" button in header
4. Click "Recreate Plugin"
5. **Expected**: Modal appears showing previous error
6. Modify description: Add "improved version"
7. Click "Recreate Plugin" button
8. **Expected**: Loading spinner appears
9. **Expected**: Success message and page reload
10. **Expected**: Plugin regenerates and compiles

**Status**: ✅ If recreation successful

## All Upgrade Features

### Upgrade 1: AI Modification Triggers

These phrases trigger AI code modification:
- "Modify the code to..."
- "Change the message to..."
- "Update the command to..."
- "Fix the bug where..."
- "Improve the..."
- "Add feature..."
- "Edit the..."

**What happens**:
1. AI receives current code (up to 2000 chars)
2. AI generates modified code in JSON format
3. Backend validates syntax
4. Compiles with Maven
5. Creates new version in history
6. Updates download link
7. Shows success notification

### Upgrade 2: Landing Page Sections

**Navigation**: Logo + Login/Register buttons
**Hero**: Gradient background with CTAs
**Features**: 6 feature cards with icons
**How It Works**: 3-step process visualization
**Benefits**: 4 key advantages
**CTA**: Final call-to-action
**Footer**: Copyright and warnings

### Upgrade 3: Auto-Refresh Mechanics

**Interval**: 30 seconds (configurable)
**API**: `GET /api/dashboard/plugins`
**Pause**: When tab is hidden (saves resources)
**Resume**: When tab becomes visible
**Indicator**: Bottom-right corner shows refresh status
**Animation**: Smooth fade-in for updated cards

### Upgrade 4: Recreation Options

**Trigger**: Only for plugins with 'error' status
**Modal Fields**:
- Plugin Name (editable)
- Version (editable)
- Minecraft Version (dropdown)
- Description (editable)
- Features (optional, editable)

**Smart Retry**: AI receives previous error context to avoid same mistakes

## API Endpoints

### New Endpoints:
1. `GET /api/dashboard/plugins` - Returns JSON with all user plugins
2. `POST /api/plugin/<id>/recreate` - Recreates failed plugin with new parameters
3. `POST /api/chat/send` - Enhanced with modification detection

### Existing Endpoints (Still Work):
- `POST /api/generate` - Generate new plugin
- `GET /api/plugin/<id>/download` - Download compiled plugin
- `POST /login` - User login
- `POST /register` - User registration

## Troubleshooting

### Auto-Refresh Not Working
```javascript
// Check browser console (F12)
// Should see: "Auto-refresh started (30s interval)"

// If not, check:
1. Is JavaScript enabled?
2. Any console errors?
3. Is dashboard page loaded?
```

### AI Modification Not Triggering
```
Common reasons:
1. Message doesn't contain modification keywords
2. Plugin has no previous versions (no code to modify)
3. Plugin status is not 'compiled' or 'error'

Try these phrases:
- "Modify the command to send 'Test'"
- "Change the message color to red"
- "Add a new feature: ..."
```

### Recreate Button Not Showing
```
Requirements for recreate button:
1. Plugin must have status = 'error'
2. User must own the plugin
3. Must be on plugin detail page (not dashboard)

Check:
- Is plugin status 'error'?  (visible as red badge)
- Are you the plugin owner?
```

### Landing Page Shows Login Form
```
Possible causes:
1. Templates not updated properly
2. Browser cache (clear cache and reload)
3. Wrong route accessed

Solutions:
- Clear browser cache (Ctrl+Shift+Delete)
- Try incognito window
- Access root URL exactly: http://localhost:5002/
```

## Configuration Options

### Change Auto-Refresh Interval
Edit `templates/dashboard.html` around line 150:
```javascript
autoRefreshInterval = setInterval(async () => {
    await refreshDashboard();
}, 30000); // Change 30000 to desired milliseconds (e.g., 60000 for 1 minute)
```

### Change Code Context Size
Edit `app.py` around line 670:
```python
{current_code[:2000]}  # Increase 2000 to send more code to AI
# Note: Larger context = more tokens = possible API limits
```

### Change Modification Keywords
Edit `app.py` around line 660:
```python
modification_keywords = ['modify', 'change', 'update', 'edit', 'alter', 'fix', 'improve', 'add feature', 'remove', 'refactor']
# Add or remove keywords as needed
```

## Performance Tips

1. **Auto-Refresh**: Use longer intervals (60s) if server is slow
2. **Code Context**: Reduce size if hitting API token limits
3. **Database**: Add indexes for better query performance
4. **Compilation**: Ensure Maven uses multiple threads

## Security Notes

⚠️ **Important**:
1. Change default admin password immediately
2. Use strong SECRET_KEY in production
3. Never commit API keys to git
4. Always use HTTPS in production
5. Validate all user inputs

## Next Steps

1. ✅ Verify all 4 upgrades work
2. ✅ Change admin password
3. ✅ Customize landing page with your branding
4. ✅ Set production environment variables
5. ✅ Deploy to hosting platform

## Deployment

### Quick Deploy to Render:
1. Push code to GitHub
2. Create new Web Service on Render
3. Connect repository
4. Set environment variables:
   ```
   OPENROUTER_API_KEY=sk-or-v1-...
   SECRET_KEY=your-secret-key
   RENDER=true
   ```
5. Deploy

### Quick Deploy to Heroku:
```bash
heroku create pluginforge-studio
heroku addons:create heroku-postgresql:mini
heroku config:set OPENROUTER_API_KEY=sk-or-v1-...
heroku config:set SECRET_KEY=your-secret-key
git push heroku main
```

## Success Checklist

After setup, verify:
- [ ] Landing page loads (not login form)
- [ ] Can register new account
- [ ] Dashboard shows auto-refresh indicator
- [ ] Can create new plugin
- [ ] AI can modify plugin via chat
- [ ] Can recreate failed plugins
- [ ] Download buttons work
- [ ] Version history is tracked

## Support Files

- `UPGRADES_COMPLETE.md` - Full documentation of all upgrades
- `README.md` - Original project documentation
- `DEPLOY_RENDER.md` - Render deployment guide

---

**All 4 upgrades implemented and tested!** 🎉

Ready to revolutionize Minecraft plugin development with AI.
