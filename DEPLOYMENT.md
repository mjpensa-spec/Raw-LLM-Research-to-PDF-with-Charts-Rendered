# Deployment Guide - Share with Coworkers

This guide shows you how to deploy the Markdown to PDF Converter so your coworkers can access it via a simple link without installing anything.

## 🚀 Quick Deployment Options

### Option 1: Railway (Recommended - Easiest)

Railway offers free hosting with automatic deployment from GitHub.

#### Steps:

1. **Push your code to GitHub**:
   ```powershell
   cd C:\md-research-processor
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/YOUR-USERNAME/md-pdf-converter.git
   git push -u origin main
   ```

2. **Deploy to Railway**:
   - Go to https://railway.app
   - Sign up/login with GitHub
   - Click "New Project" → "Deploy from GitHub repo"
   - Select your repository
   - Railway will auto-detect the Dockerfile and deploy
   - You'll get a URL like: `https://md-pdf-converter.up.railway.app`

3. **Share the link** with your coworkers!

**Cost**: Free tier includes 500 hours/month + $5 credit

---

### Option 2: Render (Great Free Option)

Render offers free web services with automatic SSL.

#### Steps:

1. **Push code to GitHub** (same as above)

2. **Deploy to Render**:
   - Go to https://render.com
   - Sign up/login
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Configure:
     - **Name**: md-pdf-converter
     - **Environment**: Docker
     - **Instance Type**: Free
   - Click "Create Web Service"
   - You'll get a URL like: `https://md-pdf-converter.onrender.com`

3. **Share the link**!

**Cost**: Free (with some limitations - service sleeps after 15 min of inactivity)

---

### Option 3: Fly.io (Good Performance)

Fly.io offers excellent performance and generous free tier.

#### Steps:

1. **Install Fly CLI**:
   ```powershell
   powershell -Command "iwr https://fly.io/install.ps1 -useb | iex"
   ```

2. **Login and Deploy**:
   ```powershell
   cd C:\md-research-processor
   fly auth signup  # or: fly auth login
   fly launch --name md-pdf-converter
   fly deploy
   ```

3. **Get your URL**:
   ```powershell
   fly status
   ```
   URL will be: `https://md-pdf-converter.fly.dev`

**Cost**: Free tier includes 3 shared VMs

---

### Option 4: DigitalOcean App Platform

Professional option with good performance.

#### Steps:

1. **Push code to GitHub**

2. **Deploy**:
   - Go to https://cloud.digitalocean.com
   - Click "Apps" → "Create App"
   - Connect GitHub repository
   - Select Dockerfile
   - Choose $5/month plan (or free trial)
   - Deploy

**Cost**: $5/month (free trial available)

---

### Option 5: Docker on Your Own Server

If you have access to a Linux server:

#### Steps:

1. **Install Docker** on the server:
   ```bash
   curl -fsSL https://get.docker.com -o get-docker.sh
   sudo sh get-docker.sh
   ```

2. **Copy your project** to the server:
   ```powershell
   scp -r C:\md-research-processor user@your-server:/home/user/
   ```

3. **Build and run**:
   ```bash
   cd md-research-processor
   docker build -t md-pdf-converter .
   docker run -d -p 80:5000 --name md-converter md-pdf-converter
   ```

4. **Access** at: `http://your-server-ip`

---

## 🐳 Local Testing with Docker

Before deploying, test locally:

```powershell
# Build the Docker image
cd C:\md-research-processor
docker build -t md-pdf-converter .

# Run the container
docker run -p 5000:5000 md-pdf-converter

# Or use docker-compose
docker-compose up
```

Access at: http://localhost:5000

---

## 📦 What Gets Deployed?

Your deployment includes:
- ✅ Web UI (HTML/CSS/JavaScript)
- ✅ Flask backend
- ✅ All Python dependencies
- ✅ Playwright + Chromium browser
- ✅ WeasyPrint + system libraries
- ✅ Markdown processing + Mermaid rendering

**Coworkers need**: Just a web browser! 🎉

---

## 🔒 Security Considerations

For production use, consider adding:

1. **Authentication** - Add login to restrict access
2. **Rate Limiting** - Prevent abuse
3. **File Size Limits** - Already set to 16MB
4. **HTTPS** - Most platforms provide this automatically
5. **Environment Variables** - For sensitive configuration

Example: Add basic auth to `app.py`:

```python
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import check_password_hash, generate_password_hash

auth = HTTPBasicAuth()

users = {
    "admin": generate_password_hash("your-password")
}

@auth.verify_password
def verify_password(username, password):
    if username in users and check_password_hash(users.get(username), password):
        return username

@app.route('/')
@auth.login_required
def index():
    return render_template('index.html')
```

---

## 📊 Monitoring

Most platforms provide:
- **Logs** - View application logs
- **Metrics** - CPU, memory usage
- **Uptime** - Service availability
- **Alerts** - Email notifications

---

## 🆘 Troubleshooting

### Build Fails
- Check Dockerfile syntax
- Ensure all files are committed to Git
- Check platform-specific logs

### Out of Memory
- Upgrade to larger instance
- Implement file size limits (already set to 16MB)
- Add cleanup for old files (already implemented)

### Slow Performance
- Consider upgrading instance type
- Use CDN for static files
- Enable caching

---

## 💡 Recommended: Railway or Render

**For quick sharing with coworkers:**

1. ✅ **Railway** - Easiest, auto-deployment, generous free tier
2. ✅ **Render** - Free option, good for low traffic
3. ✅ **Fly.io** - Best performance, good free tier

**Steps are literally:**
1. Push to GitHub
2. Connect to Railway/Render
3. Wait 5 minutes
4. Share the URL

No configuration needed - the Dockerfile handles everything!

---

## 🎯 Example Deployment URLs

After deployment, share links like:
- `https://md-pdf-converter.up.railway.app`
- `https://md-pdf-converter.onrender.com`
- `https://md-pdf-converter.fly.dev`

Coworkers just visit the URL, upload markdown, get PDF! 🚀
