# Complete Deployment Guide - Markdown to PDF Converter

This comprehensive guide walks you through deploying your Markdown to PDF converter so coworkers can access it via a web link.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Preparing Your Code](#preparing-your-code)
3. [Railway Deployment (Recommended)](#railway-deployment-recommended)
4. [Render Deployment (Free Alternative)](#render-deployment-free-alternative)
5. [Fly.io Deployment](#flyio-deployment)
6. [DigitalOcean App Platform](#digitalocean-app-platform)
7. [Heroku Deployment](#heroku-deployment)
8. [Self-Hosted with Docker](#self-hosted-with-docker)
9. [Custom Domain Setup](#custom-domain-setup)
10. [Environment Variables](#environment-variables)
11. [Monitoring & Maintenance](#monitoring--maintenance)
12. [Troubleshooting](#troubleshooting)

---

## Prerequisites

Before deploying, ensure you have:

- ✅ A GitHub account (free) - https://github.com
- ✅ Git installed on your computer
- ✅ Your markdown processor code (already done!)
- ✅ A credit card (for some platforms, even if using free tier)

### Checking Git Installation

```powershell
git --version
```

If not installed, download from: https://git-scm.com/download/win

---

## Preparing Your Code

### Step 1: Initialize Git Repository

```powershell
# Navigate to your project
cd C:\md-research-processor

# Initialize git (if not already done)
git init

# Check status
git status
```

### Step 2: Create .gitignore (Already Created)

Verify `.gitignore` exists and contains:
```
__pycache__/
*.pyc
venv/
uploads/
outputs/
.env
```

### Step 3: Create GitHub Repository

1. Go to https://github.com
2. Click the **"+"** icon (top right) → **"New repository"**
3. Fill in details:
   - **Repository name**: `md-pdf-converter` (or your preferred name)
   - **Description**: "Convert markdown files with LLM research to PDFs with rendered visuals"
   - **Visibility**: Choose Public or Private
   - **DO NOT** initialize with README (you already have one)
4. Click **"Create repository"**

### Step 4: Push to GitHub

```powershell
# Add all files
git add .

# Commit
git commit -m "Initial commit - Markdown to PDF Converter"

# Add remote (replace YOUR-USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR-USERNAME/md-pdf-converter.git

# Push to GitHub
git branch -M main
git push -u origin main
```

**If prompted for authentication:**
- Use a Personal Access Token (not password)
- Generate at: https://github.com/settings/tokens
- Select "repo" scope
- Use token as password when prompted

### Step 5: Verify on GitHub

1. Refresh your GitHub repository page
2. You should see all your files uploaded
3. Verify `Dockerfile` is present (this is crucial!)

---

## Railway Deployment (Recommended)

**Best for**: Quick deployment, automatic updates, great free tier
**Time**: ~5-10 minutes
**Cost**: Free tier with $5 credit/month

### Why Railway?

✅ Automatically detects Dockerfile
✅ One-click deployment
✅ Auto-redeploys on git push
✅ Free SSL certificate
✅ Easy environment variable management
✅ Great free tier ($5 credit + 500 hours/month)

### Step-by-Step Instructions

#### 1. Create Railway Account

1. Go to https://railway.app
2. Click **"Login"** → **"Login with GitHub"**
3. Authorize Railway to access your GitHub account
4. Complete account setup (no credit card required for free tier)

#### 2. Create New Project

1. Click **"New Project"** button (center of dashboard)
2. Select **"Deploy from GitHub repo"**
3. If first time:
   - Click **"Configure GitHub App"**
   - Select **"All repositories"** or choose specific repo
   - Click **"Install & Authorize"**
4. Select your `md-pdf-converter` repository
5. Railway automatically detects the Dockerfile

#### 3. Configure Deployment

Railway will automatically:
- Detect the `Dockerfile`
- Build the Docker image
- Deploy the container
- Assign resources

**Wait for deployment:**
- You'll see build logs in real-time
- Build takes ~5-10 minutes (first time)
- Status will show "Active" when ready

#### 4. Generate Public Domain

1. Click on your deployed service
2. Go to **"Settings"** tab
3. Scroll to **"Networking"** section
4. Click **"Generate Domain"**
5. Railway provides a domain like: `md-pdf-converter.up.railway.app`

#### 5. Test Your Deployment

1. Click the generated domain URL
2. You should see your web interface
3. Test uploading a markdown file
4. Verify PDF generation works

#### 6. Configure Environment Variables (Optional)

1. Go to **"Variables"** tab
2. Click **"+ New Variable"**
3. Add:
   ```
   FLASK_ENV=production
   PORT=5000
   ```
4. Click **"Add"** (deployment will restart automatically)

#### 7. Share with Your Team! 🎉

Copy your Railway URL and share:

```
Hey team! 👋

I've deployed a Markdown to PDF converter:
🔗 https://md-pdf-converter.up.railway.app

Features:
✅ Upload .md files
✅ Automatic Mermaid diagram rendering
✅ Professional PDF output
✅ No installation required!

Just drag & drop your markdown files!
```

### Railway: Auto-Deployment on Updates

Every time you push to GitHub, Railway auto-deploys:

```powershell
# Make changes to your code
# ...

# Commit and push
git add .
git commit -m "Updated features"
git push

# Railway automatically redeploys! ✨
```

### Railway: Monitoring

1. **View Logs**: Click "Deployments" → Select deployment → View logs
2. **Metrics**: See CPU, memory, and network usage
3. **Incidents**: Get notified of crashes

### Railway: Cost Management

**Free Tier includes:**
- $5 credit per month
- 500 execution hours
- Unlimited projects
- Community support

**Monitoring usage:**
1. Click your profile → **"Account"**
2. View **"Usage"** tab
3. See credit consumption

**If you exceed free tier:**
- Add payment method
- Pay only for what you use
- ~$5-10/month for small team tools

---

## Render Deployment (Free Alternative)

**Best for**: Zero-cost hosting (with limitations)
**Time**: ~10-15 minutes
**Cost**: Free tier available

### Why Render?

✅ Completely free tier
✅ Automatic HTTPS
✅ Auto-deploys from GitHub
✅ Good documentation

⚠️ **Limitations:**
- Free instances sleep after 15 minutes of inactivity
- First request after sleep takes ~30 seconds to wake up
- 750 hours/month free compute

### Step-by-Step Instructions

#### 1. Create Render Account

1. Go to https://render.com
2. Click **"Get Started"**
3. Click **"Sign up with GitHub"**
4. Authorize Render

#### 2. Create Web Service

1. Click **"New +"** (top right)
2. Select **"Web Service"**
3. Click **"Connect account"** if needed
4. Find your `md-pdf-converter` repository
5. Click **"Connect"**

#### 3. Configure Service

Fill in the configuration:

- **Name**: `md-pdf-converter` (or your choice)
- **Region**: Choose closest to your users
- **Branch**: `main`
- **Runtime**: **Docker** ⚠️ Important!
- **Instance Type**: **Free**

**Advanced Settings** (expand):
- **Docker Build Context Path**: `.` (period)
- **Dockerfile Path**: `./Dockerfile`
- **Docker Command**: Leave empty (uses CMD from Dockerfile)

#### 4. Environment Variables

Click **"Advanced"** → Add environment variables:

```
FLASK_ENV=production
PORT=10000
```

**Note**: Render uses port 10000 by default

#### 5. Create Web Service

1. Click **"Create Web Service"**
2. Wait for build (10-15 minutes first time)
3. Watch build logs in real-time
4. Status shows "Live" when ready

#### 6. Get Your URL

Your service URL: `https://md-pdf-converter.onrender.com`

Click the URL to test!

#### 7. Keep Service Awake (Optional)

Free instances sleep after 15 min. To keep awake:

**Option A: Use a health check service**
- https://uptimerobot.com (free, checks every 5 minutes)
- Add your Render URL: `https://your-app.onrender.com/api/health`

**Option B: Upgrade to paid tier**
- $7/month for always-on instance
- No cold starts

### Render: Auto-Deploy Settings

1. Go to your service
2. Click **"Settings"**
3. Under **"Build & Deploy"**:
   - **Auto-Deploy**: Yes (default)
   - Deploys automatically on git push

### Render: Viewing Logs

1. Click **"Logs"** tab
2. Real-time logs
3. Filter by severity (error, warning, info)

---

## Fly.io Deployment

**Best for**: Global edge deployment, good performance
**Time**: ~15 minutes
**Cost**: Free tier (3 shared VMs)

### Why Fly.io?

✅ Excellent performance
✅ Global edge network
✅ Good free tier
✅ Simple CLI

### Step-by-Step Instructions

#### 1. Install Fly CLI

**Windows (PowerShell):**
```powershell
powershell -Command "iwr https://fly.io/install.ps1 -useb | iex"
```

**Verify installation:**
```powershell
fly version
```

Close and reopen PowerShell if command not found.

#### 2. Create Fly.io Account

```powershell
fly auth signup
```

Or login if you have an account:
```powershell
fly auth login
```

Your browser will open for authentication.

#### 3. Navigate to Project

```powershell
cd C:\md-research-processor
```

#### 4. Launch Application

```powershell
fly launch
```

**Interactive prompts:**

1. **App Name**: Enter `md-pdf-converter` (or your choice)
2. **Organization**: Select your organization
3. **Region**: Choose closest to your users
4. **PostgreSQL database**: No
5. **Redis database**: No
6. **Deploy now**: Yes

Fly.io will:
- Detect your Dockerfile
- Create `fly.toml` configuration
- Build and deploy

#### 5. Verify Deployment

```powershell
fly status
```

Get your URL:
```powershell
fly open
```

This opens your app in the browser!

#### 6. View Logs

```powershell
fly logs
```

#### 7. Set Environment Variables

```powershell
fly secrets set FLASK_ENV=production
```

#### 8. Scale Resources (Optional)

**View current scaling:**
```powershell
fly scale show
```

**Adjust memory (if needed):**
```powershell
fly scale memory 512
```

### Fly.io: Updating Your App

```powershell
# Make code changes
# Commit to git

# Deploy updates
fly deploy
```

### Fly.io: Custom Domain

```powershell
fly certs add yourdomain.com
```

Follow DNS instructions provided.

### Fly.io: Cost Management

**Free tier includes:**
- 3 shared-cpu-1x VMs
- 160GB outbound data transfer
- Free SSL certificates

**Monitor usage:**
```powershell
fly dashboard
```

---

## DigitalOcean App Platform

**Best for**: Professional hosting, predictable pricing
**Time**: ~10 minutes
**Cost**: $5/month (free trial available)

### Why DigitalOcean?

✅ Professional infrastructure
✅ Predictable pricing
✅ Great support
✅ Easy to use dashboard

### Step-by-Step Instructions

#### 1. Create DigitalOcean Account

1. Go to https://cloud.digitalocean.com
2. Sign up (credit card required, but $200 free credit for 60 days)
3. Verify email

#### 2. Create New App

1. Click **"Apps"** in left sidebar
2. Click **"Create App"**
3. Choose **"GitHub"** as source
4. Click **"Manage Access"** → Authorize DigitalOcean
5. Select your `md-pdf-converter` repository
6. Select branch: `main`
7. **Autodeploy**: Check "Autodeploy code changes"
8. Click **"Next"**

#### 3. Configure Resources

1. DigitalOcean detects Dockerfile automatically
2. **Resource Type**: Web Service
3. **HTTP Port**: 5000
4. **HTTP Request Routes**: /
5. Click **"Next"**

#### 4. Set Environment Variables

Click **"Edit"** next to environment variables:

Add:
```
FLASK_ENV=production
PORT=8080
```

Click **"Save"**

#### 5. Choose Plan

1. **Basic**: $5/month (recommended)
2. **Professional**: $12/month (better performance)
3. Choose your plan
4. Click **"Next"**

#### 6. Review and Launch

1. Review configuration
2. App name: `md-pdf-converter`
3. Click **"Create Resources"**
4. Wait for deployment (5-10 minutes)

#### 7. Access Your App

Your URL: `https://md-pdf-converter-xxxxx.ondigitalocean.app`

Click to test!

### DigitalOcean: Monitoring

1. Go to **"Apps"** → Your app
2. View:
   - **Insights**: Performance metrics
   - **Runtime Logs**: Application logs
   - **Deployments**: Build history
   - **Settings**: Configuration

### DigitalOcean: Custom Domain

1. Go to **"Settings"** → **"Domains"**
2. Click **"Add Domain"**
3. Enter your domain
4. Update DNS records (instructions provided)

---

## Heroku Deployment

**Best for**: Enterprise features
**Time**: ~15 minutes
**Cost**: $7/month (no free tier as of 2022)

### Step-by-Step Instructions

#### 1. Install Heroku CLI

Download from: https://devcenter.heroku.com/articles/heroku-cli

**Verify installation:**
```powershell
heroku --version
```

#### 2. Login to Heroku

```powershell
heroku login
```

Browser opens for authentication.

#### 3. Create Heroku App

```powershell
cd C:\md-research-processor

heroku create md-pdf-converter
```

#### 4. Set Stack to Container

```powershell
heroku stack:set container -a md-pdf-converter
```

#### 5. Add heroku.yml

Create `heroku.yml` in project root:

```yaml
build:
  docker:
    web: Dockerfile
run:
  web: python app.py
```

```powershell
git add heroku.yml
git commit -m "Add heroku.yml"
```

#### 6. Deploy

```powershell
git push heroku main
```

#### 7. Open App

```powershell
heroku open
```

#### 8. View Logs

```powershell
heroku logs --tail
```

### Heroku: Environment Variables

```powershell
heroku config:set FLASK_ENV=production
```

---

## Self-Hosted with Docker

**Best for**: Full control, existing infrastructure
**Time**: ~30 minutes
**Cost**: Server costs only

### Prerequisites

- A Linux server (Ubuntu recommended)
- SSH access
- Docker installed

### Step-by-Step Instructions

#### 1. Connect to Your Server

```powershell
ssh username@your-server-ip
```

#### 2. Install Docker (if not installed)

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Add user to docker group
sudo usermod -aG docker $USER

# Log out and back in for group to take effect
exit
```

SSH back in.

#### 3. Install Docker Compose

```bash
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
docker-compose --version
```

#### 4. Clone Your Repository

```bash
cd /opt
sudo git clone https://github.com/YOUR-USERNAME/md-pdf-converter.git
cd md-pdf-converter
```

#### 5. Create .env File

```bash
sudo nano .env
```

Add:
```
FLASK_ENV=production
PORT=5000
```

Save: `Ctrl+X`, `Y`, `Enter`

#### 6. Build and Run

```bash
# Build image
sudo docker build -t md-pdf-converter .

# Run container
sudo docker run -d \
  --name md-converter \
  --restart unless-stopped \
  -p 80:5000 \
  --env-file .env \
  md-pdf-converter

# Check status
sudo docker ps
```

#### 7. Test

Open browser: `http://your-server-ip`

#### 8. View Logs

```bash
sudo docker logs md-converter -f
```

### Using Docker Compose (Recommended)

```bash
# Start services
sudo docker-compose up -d

# View logs
sudo docker-compose logs -f

# Stop services
sudo docker-compose down

# Restart
sudo docker-compose restart
```

### SSL with Nginx and Let's Encrypt

#### 1. Install Nginx

```bash
sudo apt install nginx -y
```

#### 2. Configure Nginx

```bash
sudo nano /etc/nginx/sites-available/md-converter
```

Add:
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        client_max_body_size 20M;
    }
}
```

```bash
# Enable site
sudo ln -s /etc/nginx/sites-available/md-converter /etc/nginx/sites-enabled/

# Test configuration
sudo nginx -t

# Restart Nginx
sudo systemctl restart nginx
```

#### 3. Install Let's Encrypt SSL

```bash
sudo apt install certbot python3-certbot-nginx -y

sudo certbot --nginx -d your-domain.com

# Follow prompts
```

Now access via: `https://your-domain.com`

### Updating Self-Hosted Deployment

```bash
cd /opt/md-pdf-converter
sudo git pull
sudo docker-compose down
sudo docker-compose build
sudo docker-compose up -d
```

---

## Custom Domain Setup

### Railway

1. Go to your project → **"Settings"**
2. Click **"Networking"** → **"Custom Domain"**
3. Enter your domain: `convert.yourdomain.com`
4. Add CNAME record to your DNS:
   ```
   Type: CNAME
   Name: convert
   Value: [provided by Railway]
   ```
5. Wait for DNS propagation (5-60 minutes)

### Render

1. Go to **"Settings"** → **"Custom Domain"**
2. Click **"Add Custom Domain"**
3. Enter domain
4. Add DNS records as instructed

### Fly.io

```powershell
fly certs add yourdomain.com
```

Add DNS records as shown.

---

## Environment Variables

### Common Variables

```
FLASK_ENV=production          # Disables debug mode
PORT=5000                     # Server port
MAX_CONTENT_LENGTH=16777216   # Max file size (16MB)
```

### Setting Variables by Platform

**Railway**: Variables tab → Add variable
**Render**: Environment section during setup
**Fly.io**: `fly secrets set KEY=value`
**DigitalOcean**: App Settings → Environment Variables
**Docker**: `.env` file or `docker run -e KEY=value`

---

## Monitoring & Maintenance

### Health Checks

All platforms support health checks. Your app has:
```
GET /api/health
```

Returns: `{"status": "ok", "message": "..."}`

### Logging

**View logs by platform:**

- **Railway**: Deployments → View logs
- **Render**: Logs tab
- **Fly.io**: `fly logs`
- **DigitalOcean**: Runtime Logs
- **Docker**: `docker logs md-converter`

### Metrics to Monitor

1. **Response Time**: Should be <2 seconds
2. **Error Rate**: Should be <1%
3. **Memory Usage**: Should stay under 512MB
4. **CPU Usage**: Should average <50%

### Alerts

Set up alerts for:
- Service downtime
- High error rates
- Memory/CPU spikes

**UptimeRobot** (free): https://uptimerobot.com
- Checks every 5 minutes
- Email/SMS alerts
- Status page

---

## Troubleshooting

### Build Failures

**Problem**: Docker build fails

**Solutions**:
1. Check Dockerfile syntax
2. Verify all files committed to Git
3. Check platform-specific build logs
4. Ensure requirements.txt is correct

**Common error**: `requirements.txt not found`
```powershell
# Verify file exists
ls requirements.txt

# Ensure it's committed
git add requirements.txt
git commit -m "Add requirements"
git push
```

### Application Won't Start

**Problem**: App builds but doesn't start

**Check**:
1. Logs for error messages
2. PORT environment variable
3. Dockerfile CMD command

**Fix PORT issues**:
```python
# app.py should have:
port = int(os.environ.get('PORT', 5000))
app.run(host='0.0.0.0', port=port)
```

### Mermaid Rendering Fails

**Problem**: PDFs generate but no diagrams

**Solutions**:
1. Verify Playwright installed in Docker
2. Check container has enough memory (512MB minimum)
3. Review application logs

**Docker build check**:
```dockerfile
# Ensure Dockerfile has:
RUN playwright install chromium
RUN playwright install-deps chromium
```

### Out of Memory

**Problem**: Application crashes with OOM error

**Solutions**:
1. Upgrade instance size
2. Reduce file size limit
3. Implement better cleanup

**Railway**: Settings → Increase memory
**Render**: Upgrade to paid tier
**Fly.io**: `fly scale memory 512`

### Slow Performance

**Problem**: PDF generation takes too long

**Solutions**:
1. Upgrade instance type
2. Optimize image processing
3. Add caching

### File Upload Fails

**Problem**: Large files won't upload

**Check**:
1. `MAX_CONTENT_LENGTH` setting (16MB default)
2. Platform file size limits
3. Timeout settings

**Increase limit**:
```python
app.config['MAX_CONTENT_LENGTH'] = 32 * 1024 * 1024  # 32MB
```

### SSL Certificate Issues

**Problem**: HTTPS not working

**Solutions**:
- Railway/Render: Automatic, wait 5-10 minutes
- Custom domain: Verify DNS propagation
- Self-hosted: Check Let's Encrypt renewal

**Check DNS propagation**:
https://dnschecker.org

### Cannot Access Application

**Problem**: URL not loading

**Checklist**:
1. ✅ Is app deployed? (Check platform dashboard)
2. ✅ Is app running? (Check logs)
3. ✅ Correct URL? (Verify domain)
4. ✅ Firewall issues? (Try different network)
5. ✅ DNS propagated? (If custom domain)

---

## Security Best Practices

### 1. Environment Variables

Never commit sensitive data:
```
# .gitignore should have:
.env
*.key
secrets.py
```

### 2. File Upload Validation

Already implemented:
- File type restrictions (.md only)
- Size limits (16MB)
- Automatic cleanup

### 3. Rate Limiting (Optional)

Add Flask-Limiter:
```python
from flask_limiter import Limiter

limiter = Limiter(app, key_func=lambda: request.remote_addr)

@app.route('/api/upload', methods=['POST'])
@limiter.limit("10 per minute")
def upload_file():
    # ...
```

### 4. Authentication (Optional)

For internal tools, add basic auth:
```python
from flask_httpauth import HTTPBasicAuth

auth = HTTPBasicAuth()

users = {"admin": "generate_password_hash_here"}

@auth.verify_password
def verify(username, password):
    # ...

@app.route('/')
@auth.login_required
def index():
    # ...
```

---

## Cost Comparison

| Platform | Free Tier | Paid Tier | Best For |
|----------|-----------|-----------|----------|
| **Railway** | $5 credit/month | Pay-as-you-go | Quick deployment |
| **Render** | 750 hrs (sleeps) | $7/month | Zero cost start |
| **Fly.io** | 3 VMs | Pay-as-you-go | Performance |
| **DigitalOcean** | $200 trial | $5/month | Professional |
| **Heroku** | None | $7/month | Enterprise features |
| **Self-hosted** | N/A | Server costs | Full control |

---

## Getting Help

### Platform Support

- **Railway**: https://railway.app/discord
- **Render**: https://render.com/docs
- **Fly.io**: https://community.fly.io
- **DigitalOcean**: https://www.digitalocean.com/community

### Application Issues

Check logs first:
```powershell
# Railway: Dashboard → Logs
# Render: Logs tab
# Fly.io: fly logs
# Docker: docker logs md-converter
```

### Common Error Messages

**"ModuleNotFoundError"**: 
- Missing dependency in requirements.txt
- Rebuild container

**"Port already in use"**:
- Change PORT environment variable
- Check conflicting services

**"Permission denied"**:
- File permissions issue
- Docker volume permissions

---

## Conclusion

**Recommended Path for Most Users:**

1. ✅ **Railway** - Deploy in 5 minutes, free tier, auto-updates
2. ✅ Test with coworkers
3. ✅ Monitor usage
4. ✅ Upgrade if needed

**Your team gets:**
- 🔗 Simple URL to share
- 📱 Works on any device
- 🚀 No installation
- 🎨 Professional interface
- 🔄 Automatic updates

**Share this:**
```
Hi team! 👋

Markdown to PDF Converter is live:
🔗 https://your-app.up.railway.app

Upload your .md files → Get professional PDFs!
✅ Renders Mermaid diagrams
✅ Fixes syntax automatically
✅ No installation needed

Questions? Let me know!
```

---

**Need help?** Open an issue on GitHub or check the troubleshooting section above.

**Happy deploying!** 🚀
