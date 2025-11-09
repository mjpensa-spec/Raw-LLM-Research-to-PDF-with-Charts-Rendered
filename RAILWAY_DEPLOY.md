# Complete Railway Deployment Guide

The easiest way to share with coworkers - detailed step-by-step instructions with troubleshooting!

## 📋 Table of Contents

1. [Prerequisites](#prerequisites)
2. [Part 1: Prepare Your Code](#part-1-prepare-your-code)
3. [Part 2: Create GitHub Repository](#part-2-create-github-repository)
4. [Part 3: Deploy to Railway](#part-3-deploy-to-railway)
5. [Part 4: Configure Your Deployment](#part-4-configure-your-deployment)
6. [Part 5: Test Your Application](#part-5-test-your-application)
7. [Part 6: Share with Team](#part-6-share-with-team)
8. [Updating Your Deployment](#updating-your-deployment)
9. [Monitoring & Troubleshooting](#monitoring--troubleshooting)
10. [Advanced Configuration](#advanced-configuration)

---

## 🆘 Quick Troubleshooting

**Common Issue: "I don't see my files in GitHub after pushing"**

👉 **[Jump to detailed solution](#step-31b-troubleshooting---files-not-showing-in-github)**

**Quick checks:**
```powershell
# Run the diagnostic script
.\check-github.ps1

# Or manually check:
# 1. Verify files were added to Git
git ls-files

# 2. Check push was successful
git log --oneline

# 3. Verify remote URL
git remote -v

# 4. Try force push if needed
git push -u origin main --force
```

Then refresh GitHub in your browser (Ctrl + F5)

---

## Prerequisites

Before you begin, make sure you have:

- ✅ A **GitHub account** (free) - [Sign up here](https://github.com/join)
- ✅ A **Railway account** (free) - [Sign up here](https://railway.app)
- ✅ **Git installed** on your computer
  - Check: Open PowerShell and run `git --version`
  - If not installed: Download from [git-scm.com](https://git-scm.com/download/win)
- ✅ Your markdown processor code at `C:\md-research-processor`

**Time required:** 10-15 minutes for first-time deployment

---

## Part 1: Prepare Your Code

### Step 1.1: Verify Your Files

Open PowerShell and navigate to your project:

```powershell
cd C:\md-research-processor
```

Verify you have all required files:

```powershell
dir
```

You should see these key files:
- ✅ `Dockerfile` - Container configuration
- ✅ `app.py` - Flask application
- ✅ `requirements.txt` - Python dependencies
- ✅ `templates/` folder - HTML files
- ✅ `static/` folder - CSS/JS files

### Step 1.2: Initialize Git Repository

If you haven't already initialized Git:

```powershell
# Initialize Git in your project
git init

# Check Git status
git status
```

You should see a message saying you're on branch `main` or `master`.

### Step 1.3: Review .gitignore

Make sure you have a `.gitignore` file to exclude unnecessary files:

```powershell
# Check if .gitignore exists
cat .gitignore
```

It should exclude folders like `__pycache__/`, `venv/`, `uploads/`, etc.

---

## Part 2: Create GitHub Repository

### Step 2.1: Create Repository on GitHub

1. **Go to GitHub**: Open [github.com](https://github.com) in your browser
2. **Sign in** to your account
3. **Click the "+" icon** in the top-right corner
4. **Select "New repository"**

### Step 2.2: Configure Repository Settings

Fill in the repository details:

- **Repository name**: `Raw-LLM-Research-to-PDF-with-Charts-Rendered`
- **Description**: `Convert markdown files to PDFs with rendered Mermaid diagrams`
- **Visibility**: 
  - ✅ **Public** (recommended for easy deployment)
  - Or **Private** (if you have concerns about code visibility)
- **Initialize repository**: 
  - ❌ **DO NOT** check "Add a README file"
  - ❌ **DO NOT** add .gitignore (you already have one)
  - ❌ **DO NOT** choose a license yet

Click **"Create repository"**

### Step 2.3: Copy Repository URL

After creating the repository, you'll see quick setup instructions. Copy the **HTTPS URL** that looks like:

```
https://github.com/YOUR-USERNAME/Raw-LLM-Research-to-PDF-with-Charts-Rendered.git
```

Keep this URL handy!

---

## Part 3: Deploy to Railway

### Step 3.1: Push Code to GitHub

Back in PowerShell, in your project directory:

```powershell
# Make sure you're in the right directory
cd C:\md-research-processor

# Add all files to Git
git add .

# Check what will be committed
git status

# Commit your code
git commit -m "Initial commit - Markdown to PDF Converter with web UI"

# Add GitHub as remote (replace YOUR-USERNAME with your actual GitHub username)
git remote add origin https://github.com/YOUR-USERNAME/Raw-LLM-Research-to-PDF-with-Charts-Rendered.git

# Push to GitHub
git branch -M main
git push -u origin main
```

**What if it asks for credentials?**
- GitHub no longer accepts passwords - you need a **Personal Access Token**
- Go to: GitHub Settings → Developer settings → Personal access tokens → Tokens (classic)
- Click "Generate new token (classic)"
- Select scopes: `repo` (all checkboxes under repo)
- Copy the token and use it as your password

**Verify:** Go to your GitHub repository URL - you should see all your files!

### Step 3.1b: Troubleshooting - Files Not Showing in GitHub

**If you don't see your files on GitHub, follow these steps:**

#### Check 1: Verify the Push Was Successful

Look at the output from `git push`. You should see:

```
Enumerating objects: 25, done.
Counting objects: 100% (25/25), done.
Delta compression using up to 8 threads
Compressing objects: 100% (20/20), done.
Writing objects: 100% (25/25), 15.23 KiB | 1.52 MiB/s, done.
Total 25 (delta 2), reused 0 (delta 0)
To https://github.com/YOUR-USERNAME/md-pdf-converter.git
 * [new branch]      main -> main
```

**If you see errors instead:**
- `error: failed to push` - Check your credentials
- `Permission denied` - Verify your Personal Access Token has `repo` permissions
- `remote: Repository not found` - Check your repository URL

#### Check 2: Verify Your Current Branch

```powershell
# Check which branch you're on
git branch

# You should see:
# * main (with an asterisk)
```

**If you're on a different branch** (like `master`):
```powershell
# Push from your current branch
git push -u origin master
```

#### Check 3: View Your Files Locally in Git

```powershell
# Check what files Git is tracking
git ls-files

# You should see all your files listed:
# app.py
# main.py
# Dockerfile
# requirements.txt
# templates/index.html
# static/style.css
# etc.
```

**If you don't see your files**, they weren't added to Git:
```powershell
# Check untracked files
git status

# If you see files under "Untracked files:", add them:
git add .
git commit -m "Add all files"
git push
```

#### Check 4: Visit GitHub and Refresh

1. **Go to your repository URL**: `https://github.com/YOUR-USERNAME/md-pdf-converter`
2. **Make sure you're on the correct branch**:
   - Look for the branch dropdown (usually says "main" or "master")
   - Click it and select the branch you pushed to
3. **Force refresh** your browser:
   - Windows: `Ctrl + F5`
   - Or click the refresh button

#### Check 5: Verify Repository URL

```powershell
# Check your remote URL
git remote -v

# You should see:
# origin  https://github.com/YOUR-USERNAME/Raw-LLM-Research-to-PDF-with-Charts-Rendered.git (fetch)
# origin  https://github.com/YOUR-USERNAME/Raw-LLM-Research-to-PDF-with-Charts-Rendered.git (push)
```

**If the URL is wrong**:
```powershell
# Remove the wrong remote
git remote remove origin

# Add the correct one (replace YOUR-USERNAME with your actual GitHub username)
git remote add origin https://github.com/YOUR-USERNAME/Raw-LLM-Research-to-PDF-with-Charts-Rendered.git

# Try pushing again
git push -u origin main
```

#### Check 6: View Commit History on GitHub

1. **Go to your GitHub repository**: `https://github.com/YOUR-USERNAME/Raw-LLM-Research-to-PDF-with-Charts-Rendered`
2. **Click on "Commits"** (shows a clock icon with a number)
3. **You should see your commit**: "Initial commit - Markdown to PDF Converter with web UI"
4. **Click on the commit** to see what files were included

**If you see the commit but no files**:
- The commit might be empty
- Run `git log --stat` locally to see what was committed

#### Complete Verification Checklist

Run these commands to verify everything:

```powershell
# 1. Check what files are staged
git status

# 2. Check what files Git is tracking
git ls-files

# 3. Check your remote
git remote -v

# 4. Check your recent commits
git log --oneline -5

# 5. Check what was in your last commit
git show --stat
```

#### Still Having Issues? Here's the Reset Solution

If nothing works, let's start fresh:

```powershell
# Navigate to your project
cd C:\md-research-processor

# Check what's in the directory
dir

# Make sure you have a .git folder
dir -Force

# If you see .git folder, check status
git status

# Add ALL files (including hidden ones)
git add -A

# Commit everything
git commit -m "Complete project files"

# Force push (use with caution!)
git push -u origin main --force
```

**After force pushing:**
1. Wait 10 seconds
2. Refresh GitHub in your browser (Ctrl + F5)
3. Check if files appear

#### Visual Guide: What You Should See on GitHub

When you visit `https://github.com/YOUR-USERNAME/Raw-LLM-Research-to-PDF-with-Charts-Rendered`, you should see:

**Files visible:**
- ✅ `app.py`
- ✅ `main.py`
- ✅ `Dockerfile`
- ✅ `docker-compose.yml`
- ✅ `requirements.txt`
- ✅ `README.md`
- ✅ `templates/` folder
- ✅ `static/` folder
- ✅ Other Python files (markdown_fixer.py, etc.)

**Count check:** You should see **15-20 files/folders** in total

### Step 3.2: Sign Up for Railway

1. **Go to Railway**: Open [railway.app](https://railway.app) in your browser
2. **Click "Login"** or "Start a New Project"
3. **Sign in with GitHub** (recommended)
   - This allows Railway to access your repositories
   - Click "Authorize Railway" when prompted
4. **Complete account setup** if it's your first time

### Step 3.3: Create New Project on Railway

1. **On Railway Dashboard**, click **"New Project"** button (purple button)
2. **Select "Deploy from GitHub repo"**
   - If you don't see your repositories, click "Configure GitHub App" to grant access
3. **Find and select** your `Raw-LLM-Research-to-PDF-with-Charts-Rendered` repository from the list
4. **Click on the repository** to start deployment

### Step 3.4: Watch the Build Process

Railway will now automatically:

1. **Detect your Dockerfile** ✅
   - You'll see: "Dockerfile detected"
2. **Clone your repository** ✅
3. **Build the Docker container** ✅
   - This takes 3-5 minutes
   - You'll see logs showing:
     - Installing system dependencies (WeasyPrint, Playwright)
     - Installing Python packages
     - Downloading Chromium browser
4. **Deploy the application** ✅
5. **Start the service** ✅

**Watch the logs** in the "Deployments" tab - you'll see:
```
[INFO] Installing dependencies...
[INFO] Playwright browsers installed
[INFO] Starting Flask application
[INFO] Running on 0.0.0.0:5000
```

When you see **"SUCCESS"** with a green checkmark, your deployment is complete!

---

## Part 4: Configure Your Deployment

### Step 4.1: Generate Public Domain

Your app is deployed but not yet accessible publicly. Let's fix that:

1. **Click on your service** in the Railway dashboard (it shows your repo name)
2. **Go to the "Settings" tab**
3. **Scroll down to "Networking" section**
4. **Find "Public Networking"**
5. **Click "Generate Domain"**

Railway will create a URL like:
```
https://raw-llm-research-to-pdf-with-charts-rendered-production-XXXX.up.railway.app
```

Or Railway might shorten it to something like:
```
https://your-app-name.up.railway.app
```

This is your **public URL** - save it!

### Step 4.2: Set Environment Variables (Optional but Recommended)

1. Still in your service, **click the "Variables" tab**
2. **Click "New Variable"**
3. **Add these variables**:

| Variable Name | Value | Purpose |
|--------------|-------|---------|
| `FLASK_ENV` | `production` | Disables debug mode |
| `PORT` | `5000` | Server port (Railway auto-detects this) |

4. **Click "Add"** for each variable

Railway will automatically restart your service with the new variables.

### Step 4.3: Verify Health Check

1. **Go to "Deployments" tab**
2. **Click on the latest deployment** (should show "Active")
3. **Check the logs** - you should see:
   ```
   ============================================================
   Markdown to PDF Converter - Web UI
   ============================================================
   Environment: production
   Server starting at: http://0.0.0.0:5000
   ```

---

## Part 5: Test Your Application

### Step 5.1: Open Your Application

1. **Copy your Railway domain** (from Settings → Networking)
2. **Open it in a browser**: `https://your-app.up.railway.app`

You should see:
- ✅ The beautiful gradient purple background
- ✅ "Markdown to PDF Converter" heading
- ✅ File upload area
- ✅ Three feature boxes at the bottom

### Step 5.2: Test File Upload

Let's test with the example file:

1. **Download** or prepare a markdown file (you can use `example_input.md`)
2. **Drag the file** onto the upload area or click to browse
3. **Click "Convert to PDF"**
4. **Watch the progress** - you should see:
   - "Processing your file..."
   - "Fixing markdown syntax..."
   - "Rendering Mermaid diagrams..."
   - "Generating PDF..."
5. **PDF downloads automatically!**

### Step 5.3: Verify PDF Output

Open the downloaded PDF and verify:
- ✅ All text is properly formatted
- ✅ Mermaid diagrams are rendered as images (not code)
- ✅ Tables are formatted nicely
- ✅ No raw code blocks that should be visuals
- ✅ Professional styling

**Success!** 🎉 Your application is working!

---

## Part 6: Share with Team

### Step 6.1: Copy Your Public URL

Your Railway domain is the link you'll share:
```
https://md-pdf-converter-production-XXXX.up.railway.app
```

### Step 6.2: Create a Team Message

Here's a template message to send your coworkers:

```
Hey team! 👋

I've deployed a Markdown to PDF Converter for our LLM research outputs.

🔗 Link: https://your-app.up.railway.app

✨ Features:
✅ Automatically fixes markdown syntax issues
✅ Renders all Mermaid diagrams (flowcharts, sequence diagrams, etc.)
✅ Generates professional PDFs ready for sharing
✅ Works in any browser - no installation needed!

📝 How to use:
1. Click the link
2. Upload your .md file (drag & drop works too!)
3. Click "Convert to PDF"
4. PDF downloads automatically

Perfect for converting our LLM research outputs to presentation-ready documents!

Questions? Let me know!
```

### Step 6.3: Optional - Add to Bookmarks/Wiki

Consider adding the link to:
- Team Slack/Teams channel (pinned message)
- Company wiki or documentation
- Team bookmarks/shortcuts
- Email signature

---

## Updating Your Deployment

### When You Make Code Changes

Railway automatically redeploys when you push to GitHub:

```powershell
# Make your changes to the code
# Then commit and push

cd C:\md-research-processor

# Stage changes
git add .

# Commit with descriptive message
git commit -m "Added new feature: custom PDF styling"

# Push to GitHub
git push
```

**Railway will**:
1. Detect the push
2. Rebuild the Docker container
3. Deploy the new version
4. Zero downtime (keeps old version running until new one is ready)

**Watch the deployment** in Railway dashboard → Deployments tab

### Rolling Back a Deployment

If something goes wrong:

1. **Go to Railway** → Your project → **Deployments** tab
2. **Find a previous successful deployment**
3. **Click the "..." menu** on that deployment
4. **Select "Redeploy"**

Railway will roll back to that version instantly!

---

## Monitoring & Troubleshooting

### Viewing Logs

**Real-time logs:**
1. Go to Railway dashboard
2. Click your service
3. Click **"Deployments"** tab
4. Click on the **active deployment**
5. Logs stream in real-time

**What to look for:**
- ✅ `Server starting at: http://0.0.0.0:5000` - App started successfully
- ✅ `Processing your file...` - User uploads being processed
- ❌ `Error:` messages - Problems to investigate
- ❌ `ModuleNotFoundError` - Missing dependencies

### Common Issues & Solutions

#### Issue 1: "Application Error" or 503 Error

**Symptoms:** Can't access the URL, shows error page

**Solutions:**
1. **Check build logs** - Did the Docker build complete?
   - Go to Deployments → Build Logs
   - Look for errors during `pip install` or `playwright install`

2. **Check runtime logs** - Is the app crashing?
   - Look for Python errors or exceptions
   - Common: Port binding issues (already fixed in our code)

3. **Verify environment variables**
   - Make sure `PORT` isn't set to something Railway can't use
   - Railway auto-assigns PORT, so you can actually remove this variable

#### Issue 2: "Out of Memory" During Build

**Symptoms:** Build fails with memory errors

**Solutions:**
1. **Upgrade Railway plan** - Free tier has memory limits
2. **Optimize Dockerfile** - Already optimized in our version
3. **Contact Railway support** - They're very responsive

#### Issue 3: Mermaid Diagrams Not Rendering

**Symptoms:** PDFs show empty spaces where diagrams should be

**Solutions:**
1. **Check Playwright installation** in build logs
   - Should see: `playwright install chromium` succeed
2. **Check browser dependencies** 
   - Our Dockerfile includes all necessary libs
3. **Test with simple diagram** first
4. **Check Railway logs** for Playwright errors

#### Issue 4: Slow Performance

**Symptoms:** Long wait times during conversion

**Solutions:**
1. **Check Railway metrics**
   - Go to your service → Metrics tab
   - Look at CPU and memory usage
2. **Upgrade instance size** if consistently high usage
3. **Implement caching** (future enhancement)
4. **Optimize Mermaid rendering** (already async in our code)

#### Issue 5: File Upload Fails

**Symptoms:** "413 Request Entity Too Large" or upload errors

**Solutions:**
1. **Check file size** - Current limit is 16MB
   - Set in `app.py`: `app.config['MAX_CONTENT_LENGTH']`
2. **Increase limit if needed** (requires code change and redeploy)
3. **Check Railway request limits** - Very generous on Railway

### Performance Metrics

Railway provides built-in metrics:

1. **Go to your service**
2. **Click "Metrics" tab**
3. **View**:
   - CPU usage (should be low when idle)
   - Memory usage (will spike during PDF generation)
   - Network traffic
   - Request count

**Normal behavior:**
- Idle: ~50-100MB memory, <5% CPU
- Processing: 200-500MB memory spike, 20-50% CPU spike
- Should return to idle after processing

---

## Advanced Configuration

### Custom Domain (Optional)

Want to use your own domain instead of Railway's?

1. **Go to Settings** → **Networking**
2. **Click "Custom Domain"**
3. **Add your domain** (e.g., `md-converter.yourcompany.com`)
4. **Follow Railway's DNS instructions**
5. **Add CNAME record** to your DNS provider
6. **Wait for SSL certificate** (automatic via Let's Encrypt)

**Note:** Custom domains require Railway Pro plan ($5/month)

### Adding Authentication

Want to restrict access to your team only?

**Option 1: Railway's Built-in Authentication**
1. Use Railway's edge proxy authentication
2. Set up in project settings

**Option 2: Add Password Protection**

Create a new file `auth.py`:

```python
from functools import wraps
from flask import request, Response

def check_auth(username, password):
    """Check if username/password is valid"""
    return username == 'team' and password == 'your-secure-password'

def authenticate():
    """Send 401 response"""
    return Response(
        'Login required', 401,
        {'WWW-Authenticate': 'Basic realm="Login Required"'}
    )

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated
```

Then in `app.py`, add `@requires_auth` before your routes:

```python
from auth import requires_auth

@app.route('/')
@requires_auth
def index():
    return render_template('index.html')
```

### Scaling

**Current setup**: Single instance (perfect for team use)

**If you need more**:
1. **Railway Pro** - Better performance, custom domains
2. **Horizontal scaling** - Multiple instances (Railway supports this)
3. **Database** - Add Redis for caching (connect via Railway)

### Monitoring & Alerts

**Set up alerts**:
1. **Railway dashboard** → Project Settings → Notifications
2. **Enable**:
   - Deployment failures
   - High CPU/memory usage
   - Service crashes
3. **Add Slack/Discord webhook** for team notifications

### Backup Strategy

**Your code is safe** (on GitHub), but consider:

1. **Multiple GitHub remotes** - Push to backup repo
2. **Download Railway backups** - Regular exports
3. **Docker image registry** - Push to Docker Hub

---

## Cost Breakdown

### Railway Free Tier (Hobby Plan)

**What you get**:
- ✅ $5 in usage credit per month
- ✅ 500 execution hours
- ✅ 512MB RAM, shared CPU
- ✅ 100GB egress bandwidth
- ✅ Unlimited deployments
- ✅ Automatic SSL certificates

**What this means for you**:
- Perfect for **team tools** with moderate usage
- Supports approximately **~500-1000 PDF conversions/month** (estimate)
- **Always-on service** if within credit limit
- **$0 cost** if usage stays within free tier

### When You Might Need to Upgrade

**Signs to upgrade to Pro ($5/month)**:
- App sleeps or shows "out of credits"
- Need custom domain
- Want priority support
- Higher traffic (100+ conversions/day)
- Need faster build times

**Railway Pro Plan** ($5/month + usage):
- ✅ $5 execution credit included
- ✅ Priority builds
- ✅ Custom domains
- ✅ Better performance
- ✅ Team collaboration features

---

## Success Checklist

Before sharing with your team, verify:

- ✅ Application URL is accessible
- ✅ File upload works (test with example file)
- ✅ PDF generation completes successfully
- ✅ Mermaid diagrams render as images
- ✅ Downloaded PDF looks professional
- ✅ No errors in Railway logs
- ✅ Health check passes
- ✅ Application stays online (check after 10 minutes)

---

## Getting Help

### Railway Support

- **Documentation**: [docs.railway.app](https://docs.railway.app)
- **Discord Community**: Very active, helpful community
- **Support**: help@railway.app
- **Status Page**: [status.railway.app](https://status.railway.app)

### Application Issues

1. **Check logs first** - Most issues show up here
2. **Review Dockerfile** - Build problems
3. **Test locally** - `docker build . && docker run -p 5000:5000`
4. **GitHub Issues** - Document problems for future reference

---

## Next Steps

Now that your app is deployed:

1. ✅ **Test thoroughly** - Try different markdown files
2. ✅ **Share with team** - Send the link!
3. ✅ **Monitor usage** - Watch Railway metrics
4. ✅ **Gather feedback** - What features do coworkers want?
5. ✅ **Iterate** - Make improvements, push changes (auto-deploys!)

---

## Summary

**What you accomplished**:
- ✅ Deployed a fully functional web application
- ✅ No installation required for users
- ✅ Automatic scaling and HTTPS
- ✅ Free hosting (within limits)
- ✅ Continuous deployment (push to update)

**Your team can now**:
- Upload markdown files from any device
- Get professional PDFs with rendered diagrams
- No software installation needed
- Access from anywhere with internet

**You can now**:
- Update the app by pushing to GitHub
- Monitor usage via Railway dashboard
- Roll back if something breaks
- Scale up if needed

---

🎉 **Congratulations!** You've successfully deployed a production web application that your entire team can use! 🚀
