# Quick Testing Guide - PluginForge Studio v1.7

**Date:** November 15, 2025  
**Changes:** 3 Critical Fixes + Profile System Upgrade

## Quick Start

### 1. Start the Server

```bash
cd /workspace/PluginForge-Studio
python app.py
```

Server should start on: `http://localhost:5002`

---

## Test Case 1: Dashboard Empty State

**Purpose:** Verify dashboard looks professional with 0 plugins

**Steps:**
1. Create a new user account
2. Login without creating any plugins
3. Navigate to dashboard

**Expected Result:**
- Large orange puzzle piece icon (80px)
- "Start Creating Your First Plugin" heading
- Descriptive text about AI plugin generation
- Orange "Create First Plugin" button with gradient
- Professional spacing and centering (NO broken layout)

**Pass Criteria:** ✅ Dashboard is visually appealing and functional

---

## Test Case 2: Sidebar User Info Removed

**Purpose:** Verify user info only appears in header

**Steps:**
1. Login to any account
2. Navigate to any page (dashboard, plugin chat, etc.)
3. Look at bottom-left sidebar area

**Expected Result:**
- NO user email/username at bottom of sidebar
- Sidebar only shows plugin list and search
- User info ONLY in top-right header

**Pass Criteria:** ✅ No user profile section in sidebar footer

---

## Test Case 3: Download & Info Buttons Visible

**Purpose:** Verify plugin action buttons are accessible

**Steps:**
1. Login and create/select a compiled plugin
2. Open plugin chat page
3. Look at top-right area of page (fixed header)

**Expected Result:**
- Download button (↓ icon) visible for compiled plugins
- Info button (ⓘ icon) always visible
- Both buttons clickable and functional
- Download triggers file download
- Info shows plugin details modal

**Pass Criteria:** ✅ Both buttons visible and working

---

## Test Case 4: Profile Dropdown Menu

**Purpose:** Verify GitHub-style profile dropdown

**Steps:**
1. Login to any account
2. Click on user avatar in top-right header (next to username)

**Expected Result:**
- Dropdown menu appears (280px width)
- Dark theme (#3E4146) with orange border (#FC8805)
- User section at top showing:
  - Large avatar (48px)
  - Username
  - Email
- Menu items:
  - Profile (user icon)
  - Settings (cog icon)
  - **Appearance (palette icon) - RED accent**
  - **Accessibility (universal access icon) - RED accent**
- Divider line
- Sign out option at bottom (red text)
- Clicking outside closes dropdown

**Pass Criteria:** ✅ Dropdown appears, red accents present, closes on outside click

---

## Test Case 5: Dedicated Profile Page

**Purpose:** Verify full profile settings page

**Steps:**
1. Login to any account
2. Click avatar → Profile (or navigate to `/profile`)

**Expected Result:**

### Layout
- Two-column layout: sidebar (280px) + content area
- Dark sidebar with orange accents
- Light content area (#f9fafb)

### Sidebar Navigation
- Large avatar at top (80px)
- Username and email below
- 4 navigation items:
  - Public profile
  - Account
  - Appearance
  - Accessibility
- Active item highlighted with orange left border

### Public Profile Section (Default)
- Large avatar (100px)
- "Change Avatar" button
- Display Name input
- Bio textarea
- 3 statistics cards:
  - Total Plugins (count)
  - Compiled (count)
  - Member Since (date)
- Save Changes & Cancel buttons

### Account Section
- Username (read-only)
- Email field
- Current Plan badge (orange gradient)
- "View all plans" link
- Save Changes button

### Appearance Section
- Theme selector:
  - Dark (active, checkmark)
  - Light (coming soon, disabled)
- Accent Color picker:
  - Orange (active, checkmark)
  - Others (coming soon)

### Accessibility Section
- 4 toggle switches:
  - Reduce motion
  - High contrast mode
  - Larger text
  - Keyboard shortcuts (enabled by default)
- Each with description text

**Pass Criteria:** ✅ All sections render, navigation works, responsive design

---

## Test Case 6: URL Section Parameters

**Purpose:** Verify section switching via URL

**Steps:**
1. Navigate to: `/profile`
2. Navigate to: `/profile?section=account`
3. Navigate to: `/profile?section=appearance`
4. Navigate to: `/profile?section=accessibility`

**Expected Result:**
- Each URL loads correct section
- Sidebar highlights active section
- Content area updates accordingly

**Pass Criteria:** ✅ URL parameters control section display

---

## Test Case 7: Responsive Design

**Purpose:** Verify mobile compatibility

**Steps:**
1. Resize browser to mobile width (<768px)
2. Test all pages

**Expected Result:**
- Profile sidebar hidden on mobile
- Profile dropdown still functional
- Dashboard grid adapts to single column
- All buttons and text readable

**Pass Criteria:** ✅ Mobile-friendly on all pages

---

## Test Case 8: Existing Functionality Preserved

**Purpose:** Ensure no regressions

**Steps:**
1. Create new plugin
2. Modify plugin via chat
3. Download compiled plugin
4. View plugin info
5. Use dashboard auto-refresh
6. Recreate error plugin

**Expected Result:**
- All existing features work exactly as before
- No console errors
- No visual glitches

**Pass Criteria:** ✅ All existing functionality intact

---

## Common Issues & Solutions

### Issue: Dropdown not appearing
**Solution:** Check JavaScript console for errors, ensure `toggleProfileDropdown()` function exists

### Issue: Profile page 404
**Solution:** Verify `/profile` route exists in `app.py`, restart server

### Issue: Empty state not showing
**Solution:** Ensure user has 0 plugins, check CSS is loaded

### Issue: Red accents not showing
**Solution:** Check `.dropdown-item-red` class applied to correct items

---

## Success Indicators

When all tests pass, you should see:

✅ Dashboard beautiful even with 0 plugins  
✅ Clean sidebar without user info at bottom  
✅ Download and info buttons always visible  
✅ Professional dropdown menu with red accents  
✅ Complete profile page with 4 sections  
✅ Smooth navigation and interactions  
✅ Mobile responsive design  
✅ All existing features working  

---

## Production Deployment

After testing passes:

1. **Commit changes:**
   ```bash
   git add templates/dashboard.html templates/base_chat.html templates/profile.html app.py
   git commit -m "Fix 3 critical errors + add complete profile system"
   ```

2. **Deploy to production:**
   ```bash
   # Follow your standard deployment process
   # No database migrations needed (UI-only changes)
   ```

3. **Verify in production:**
   - Test all 8 test cases above
   - Monitor for errors in logs
   - Check user feedback

---

## Rollback Plan

If issues occur in production:

```bash
git revert HEAD
# Restart server
```

All changes are UI-only, so rollback is safe and immediate.

---

**Testing Time Estimate:** 15-20 minutes for complete verification  
**Required:** Modern browser, localhost access  
**Optional:** Mobile device or browser dev tools for responsive testing

---

**Status:** READY FOR TESTING  
**Version:** v1.7  
**Date:** November 15, 2025
