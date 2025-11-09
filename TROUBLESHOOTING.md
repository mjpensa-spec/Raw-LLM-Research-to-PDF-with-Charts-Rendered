# Deployment Troubleshooting Guide

Common issues and solutions when deploying the Markdown to PDF Converter.

## Table of Contents

- [Build Issues](#build-issues)
- [Runtime Issues](#runtime-issues)
- [Performance Issues](#performance-issues)
- [Platform-Specific Issues](#platform-specific-issues)
- [Network & SSL Issues](#network--ssl-issues)

---

## Build Issues

### Docker Build Fails

#### Symptom
```
Error: failed to solve with frontend dockerfile.v0
```

#### Causes & Solutions

**1. Dockerfile not found**
```powershell
# Verify Dockerfile exists in root
ls Dockerfile

# Check it's committed to git
git status
git add Dockerfile
git commit -m "Add Dockerfile"
git push
```

**2. Syntax error in Dockerfile**
- Check line endings (should be LF, not CRLF)
- Verify all commands are valid
- Use Docker Desktop to test locally:
  ```powershell
  docker build -t test .
  ```

**3. Base image unavailable**
```dockerfile
# Ensure using stable Python version
FROM python:3.11-slim
```

### Requirements Installation Fails

#### Symptom
```
ERROR: Could not find a version that satisfies the requirement...
```

#### Solutions

**1. Check requirements.txt exists**
```powershell
cat requirements.txt
```

**2. Verify package names**
- Check for typos
- Verify versions exist on PyPI
- Test locally: `pip install -r requirements.txt`

**3. Add specific versions**
```
# Instead of:
flask

# Use:
flask>=3.0.0
```

### Playwright Installation Fails

#### Symptom
```
Error: Browser not found
```

#### Solutions

**1. Verify Dockerfile has Playwright steps**
```dockerfile
RUN playwright install chromium
RUN playwright install-deps chromium
```

**2. Ensure system dependencies installed**
```dockerfile
RUN apt-get update && apt-get install -y \
    libnss3 \
    libnspr4 \
    libatk1.0-0 \
    # ... other deps
```

**3. Check available disk space**
- Playwright downloads ~300MB
- Ensure platform has enough storage

### WeasyPrint Build Fails

#### Symptom
```
error: command 'gcc' failed
```

#### Solutions

**1. Install system dependencies**
```dockerfile
RUN apt-get install -y \
    libpango-1.0-0 \
    libpangoft2-1.0-0 \
    libcairo2 \
    libgdk-pixbuf2.0-0
```

**2. Use pre-built wheels**
Already in requirements.txt:
```
weasyprint>=60.0
```

---

## Runtime Issues

### Application Won't Start

#### Symptom
Container builds but app doesn't respond.

#### Diagnostic Steps

**1. Check logs**
```powershell
# Railway: Dashboard → Deployments → View logs
# Render: Logs tab
# Fly.io:
fly logs

# Docker:
docker logs md-converter
```

**2. Look for error patterns**
- Port binding issues
- Import errors
- Missing environment variables

#### Common Causes & Fixes

**Problem: Port mismatch**
```python
# app.py should use environment PORT
port = int(os.environ.get('PORT', 5000))
app.run(host='0.0.0.0', port=port)
```

**Platform ports:**
- Railway: 5000 (default)
- Render: 10000
- Fly.io: 8080
- Heroku: Dynamic ($PORT)

**Problem: Import errors**
```
ModuleNotFoundError: No module named 'flask'
```

Solution:
```powershell
# Verify requirements.txt is complete
# Rebuild container
```

**Problem: File permissions**
```
PermissionError: [Errno 13] Permission denied
```

Solution in Dockerfile:
```dockerfile
# Create directories with correct permissions
RUN mkdir -p /tmp/md_uploads /tmp/pdf_outputs && \
    chmod 777 /tmp/md_uploads /tmp/pdf_outputs
```

### File Upload Fails

#### Symptom
"Failed to upload file" or 413 error.

#### Solutions

**1. Check file size limit**
```python
# app.py
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB
```

**2. Platform upload limits**
- Railway: 100MB
- Render: 100MB
- Fly.io: Configure in fly.toml

**3. Nginx configuration (self-hosted)**
```nginx
client_max_body_size 20M;
```

### PDF Generation Fails

#### Symptom
Upload succeeds but PDF fails to generate.

#### Diagnostic

**1. Check WeasyPrint**
```python
# Test in app logs
from weasyprint import HTML
HTML(string="<h1>Test</h1>").write_pdf("test.pdf")
```

**2. Missing fonts**
```dockerfile
# Add font support to Dockerfile
RUN apt-get install -y fonts-liberation
```

**3. Memory issues**
- Upgrade instance size
- Reduce image quality in processing

### Mermaid Diagrams Don't Render

#### Symptom
PDF generates but diagrams are missing or show errors.

#### Solutions

**1. Verify Playwright working**
```python
# Test Playwright in Python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    print("Playwright works!")
    browser.close()
```

**2. Check browser installation**
```dockerfile
# Ensure in Dockerfile:
RUN playwright install chromium
RUN playwright install-deps chromium
```

**3. Memory requirements**
- Playwright needs 512MB minimum
- Upgrade instance if needed

**4. Timeout issues**
```python
# Increase timeout in mermaid_renderer.py
await page.wait_for_timeout(5000)  # 5 seconds
```

### Cleanup Not Working

#### Symptom
Disk space fills up over time.

#### Solutions

**1. Verify cleanup function**
```python
# In app.py, ensure cleanup_old_files() is called
cleanup_old_files()
```

**2. Check file permissions**
```python
# Ensure app can delete files
os.chmod(file_path, 0o777)
```

**3. Manual cleanup (Docker)**
```bash
# Remove old files
docker exec md-converter rm -rf /tmp/md_uploads/* /tmp/pdf_outputs/*
```

---

## Performance Issues

### Slow Response Times

#### Symptom
App takes 30+ seconds to respond.

#### Solutions

**1. Cold start (Render free tier)**
- First request wakes up sleeping instance
- Upgrade to paid tier for always-on

**2. Insufficient resources**
- Check CPU/memory usage
- Upgrade instance size

**3. Large file processing**
- Optimize image compression
- Process in background queue

### High Memory Usage

#### Symptom
App crashes with OOM (Out of Memory) error.

#### Solutions

**1. Increase memory allocation**

Railway:
```
Settings → Resources → Memory: 1GB
```

Fly.io:
```powershell
fly scale memory 1024
```

Render: Upgrade to higher tier

**2. Optimize image processing**
```python
# In mermaid_renderer.py
# Use smaller viewport
await page.set_viewport_size({"width": 800, "height": 600})
```

**3. Implement garbage collection**
```python
import gc

# After processing
gc.collect()
```

### High CPU Usage

#### Symptom
CPU constantly at 100%, slow performance.

#### Solutions

**1. Profile the application**
```python
import cProfile

cProfile.run('process_file()')
```

**2. Optimize rendering**
- Cache rendered diagrams
- Process asynchronously
- Limit concurrent requests

**3. Upgrade instance**
- Move to CPU-optimized tier
- Add more CPU cores

---

## Platform-Specific Issues

### Railway Issues

#### Deployment Keeps Failing

**Check build logs:**
1. Go to deployments
2. Click failed deployment
3. Read error message

**Common fixes:**
- Verify Dockerfile syntax
- Check environment variables
- Ensure GitHub repo updated

#### Domain Not Working

**Steps:**
1. Verify domain generated
2. Check custom domain DNS settings
3. Wait for SSL certificate (5-10 min)
4. Test with curl: `curl -I https://your-app.up.railway.app`

#### Usage/Billing Issues

**Monitor usage:**
1. Profile → Usage
2. Check credit consumption
3. Set up billing alerts

### Render Issues

#### Service Keeps Sleeping

**Solution: Upgrade or use keepalive**

Use UptimeRobot:
1. Go to https://uptimerobot.com
2. Add monitor: `https://your-app.onrender.com/api/health`
3. Check every 5 minutes

#### Build Timeout

**Error: Build exceeded 15 minutes**

Solutions:
- Optimize Dockerfile (use smaller base image)
- Remove unnecessary dependencies
- Use build cache

#### Deploy Preview Not Working

**Check:**
- Pull request from same repo
- Branch configured in settings
- Build succeeds

### Fly.io Issues

#### Deployment Fails

**Check fly.toml:**
```toml
[build]
  image = "..."

[env]
  PORT = "8080"

[[services]]
  http_checks = []
  internal_port = 8080
  protocol = "tcp"
```

**Redeploy:**
```powershell
fly deploy --force
```

#### Cannot Access Logs

**Solutions:**
```powershell
# Real-time logs
fly logs

# Historical logs
fly logs --history

# Specific instance
fly logs -i instance-id
```

#### Certificate Issues

**Regenerate certificate:**
```powershell
fly certs remove yourdomain.com
fly certs add yourdomain.com
```

### DigitalOcean Issues

#### App Not Starting

**Check:**
1. Runtime logs for errors
2. HTTP port matches (8080)
3. Dockerfile CMD correct

#### Billing Surprises

**Monitor:**
1. Billing → Usage
2. Set spending limits
3. Check resource allocation

### Docker (Self-Hosted) Issues

#### Container Exits Immediately

**Debug:**
```bash
# Check logs
docker logs md-converter

# Run interactively
docker run -it md-pdf-converter /bin/bash

# Check for errors
python app.py
```

#### Port Already in Use

**Find and kill process:**
```bash
# Linux/Mac
sudo lsof -i :5000
sudo kill -9 PID

# Or use different port
docker run -p 8080:5000 md-pdf-converter
```

#### Permission Denied

**Fix permissions:**
```bash
# Give Docker user access
sudo chown -R 1000:1000 /path/to/project

# Or run as root (not recommended)
docker run --user root md-pdf-converter
```

---

## Network & SSL Issues

### Cannot Access Application

#### Symptom
URL not loading, connection refused.

#### Checklist

✅ **Is app running?**
- Check platform dashboard
- Verify status is "Active" or "Running"

✅ **Correct URL?**
- Copy URL from platform
- Check for typos
- Try in incognito mode

✅ **Firewall blocking?**
- Try different network
- Check corporate firewall
- Test with VPN

✅ **DNS issues?** (custom domain)
- Check DNS propagation: https://dnschecker.org
- Verify CNAME/A records correct
- Wait 24-48 hours for full propagation

### SSL Certificate Errors

#### Symptom
"Your connection is not private" or NET::ERR_CERT_AUTHORITY_INVALID

#### Solutions

**Railway/Render (automatic SSL):**
- Wait 10-15 minutes after deployment
- Verify domain generated correctly
- Check for mixed content warnings

**Custom domain:**
1. Verify DNS records correct
2. Check certificate status in platform
3. Force renewal if needed

**Self-hosted (Let's Encrypt):**
```bash
# Renew certificate
sudo certbot renew

# Test renewal
sudo certbot renew --dry-run

# Check nginx config
sudo nginx -t
```

### CORS Errors

#### Symptom
Browser console: "CORS policy: No 'Access-Control-Allow-Origin' header"

#### Solution

Already configured in app.py:
```python
from flask_cors import CORS
CORS(app)
```

If issues persist:
```python
CORS(app, resources={r"/*": {"origins": "*"}})
```

### Mixed Content Warnings

#### Symptom
"Mixed Content: The page was loaded over HTTPS, but requested an insecure..."

#### Solution

Ensure all resources use HTTPS:
```html
<!-- templates/index.html -->
<script src="https://cdn.example.com/script.js"></script>
```

---

## Getting More Help

### 1. Check Logs First

Always check application logs:
```powershell
# Railway: Dashboard → Logs
# Render: Logs tab
# Fly.io: fly logs
# Docker: docker logs md-converter
```

### 2. Platform Support

- **Railway**: https://railway.app/discord
- **Render**: https://render.com/docs
- **Fly.io**: https://community.fly.io
- **DigitalOcean**: https://www.digitalocean.com/community

### 3. Enable Debug Mode (Temporarily)

```python
# app.py - for local debugging only!
app.run(debug=True)
```

⚠️ **Never enable debug in production!**

### 4. Test Locally First

```powershell
# Test with Docker locally
docker build -t test-app .
docker run -p 5000:5000 test-app

# Access: http://localhost:5000
```

### 5. Minimal Reproduction

Create minimal test case:
```python
# test_app.py
from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello():
    return "Working!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

If this works, problem is in your application code.

---

## Quick Reference: Error Codes

| Code | Meaning | Common Cause |
|------|---------|--------------|
| 400 | Bad Request | Invalid file format |
| 413 | Payload Too Large | File exceeds size limit |
| 500 | Internal Server Error | Application crash |
| 502 | Bad Gateway | App not responding |
| 503 | Service Unavailable | App not running |
| 504 | Gateway Timeout | Request took too long |

---

## Preventive Measures

### 1. Health Monitoring

Use UptimeRobot or similar:
- Monitor: `https://your-app.com/api/health`
- Check every 5 minutes
- Alert on downtime

### 2. Resource Monitoring

Watch for:
- Memory usage >80%
- CPU usage consistently high
- Disk space decreasing

### 3. Regular Updates

```powershell
# Update dependencies monthly
pip list --outdated

# Update requirements.txt
pip install --upgrade package-name
pip freeze > requirements.txt

# Test and deploy
git add requirements.txt
git commit -m "Update dependencies"
git push
```

### 4. Backup Configuration

Keep local copies of:
- Environment variables
- Configuration files
- Deployment settings

---

**Still having issues?** Open an issue on GitHub with:
1. Platform (Railway/Render/etc.)
2. Error message/logs
3. Steps to reproduce
4. What you've tried

Good luck! 🚀
