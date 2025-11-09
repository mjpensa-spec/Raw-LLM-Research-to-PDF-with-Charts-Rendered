# GitHub Verification Script
# Run this to diagnose why files aren't showing in GitHub

Write-Host "=====================================" -ForegroundColor Cyan
Write-Host "GitHub Upload Diagnostic Tool" -ForegroundColor Cyan
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host ""

# Check 1: Current directory
Write-Host "[1/8] Checking current directory..." -ForegroundColor Yellow
$currentPath = Get-Location
Write-Host "    Current path: $currentPath" -ForegroundColor Gray
if ($currentPath -like "*md-research-processor*") {
    Write-Host "    ✓ In correct directory" -ForegroundColor Green
} else {
    Write-Host "    ✗ WARNING: You should be in md-research-processor directory" -ForegroundColor Red
    Write-Host "    Run: cd C:\md-research-processor" -ForegroundColor Yellow
}
Write-Host ""

# Check 2: Git initialized
Write-Host "[2/8] Checking if Git is initialized..." -ForegroundColor Yellow
if (Test-Path ".git") {
    Write-Host "    ✓ Git repository initialized" -ForegroundColor Green
} else {
    Write-Host "    ✗ Git not initialized" -ForegroundColor Red
    Write-Host "    Run: git init" -ForegroundColor Yellow
}
Write-Host ""

# Check 3: Files in directory
Write-Host "[3/8] Checking project files..." -ForegroundColor Yellow
$requiredFiles = @("app.py", "main.py", "Dockerfile", "requirements.txt")
$missingFiles = @()
foreach ($file in $requiredFiles) {
    if (Test-Path $file) {
        Write-Host "    ✓ Found $file" -ForegroundColor Green
    } else {
        Write-Host "    ✗ Missing $file" -ForegroundColor Red
        $missingFiles += $file
    }
}
Write-Host ""

# Check 4: Files tracked by Git
Write-Host "[4/8] Checking files tracked by Git..." -ForegroundColor Yellow
try {
    $trackedFiles = git ls-files 2>&1
    if ($LASTEXITCODE -eq 0) {
        $fileCount = ($trackedFiles | Measure-Object -Line).Lines
        Write-Host "    Git is tracking $fileCount files" -ForegroundColor Gray
        if ($fileCount -gt 10) {
            Write-Host "    ✓ Good number of files tracked" -ForegroundColor Green
        } else {
            Write-Host "    ⚠ Only $fileCount files tracked - might be missing some" -ForegroundColor Yellow
        }
    } else {
        Write-Host "    ✗ Error checking tracked files" -ForegroundColor Red
    }
} catch {
    Write-Host "    ✗ Cannot check tracked files" -ForegroundColor Red
}
Write-Host ""

# Check 5: Git status
Write-Host "[5/8] Checking Git status..." -ForegroundColor Yellow
try {
    $status = git status --short 2>&1
    if ($status) {
        Write-Host "    ⚠ Uncommitted changes detected:" -ForegroundColor Yellow
        Write-Host $status -ForegroundColor Gray
        Write-Host "    Action needed: Run 'git add .' and 'git commit'" -ForegroundColor Yellow
    } else {
        Write-Host "    ✓ Working directory clean" -ForegroundColor Green
    }
} catch {
    Write-Host "    ✗ Cannot check status" -ForegroundColor Red
}
Write-Host ""

# Check 6: Remote configured
Write-Host "[6/8] Checking GitHub remote..." -ForegroundColor Yellow
try {
    $remotes = git remote -v 2>&1
    if ($LASTEXITCODE -eq 0 -and $remotes) {
        Write-Host "    ✓ GitHub remote configured:" -ForegroundColor Green
        Write-Host $remotes -ForegroundColor Gray
        
        # Check if it's a valid GitHub URL
        if ($remotes -match "github.com") {
            Write-Host "    ✓ Valid GitHub URL" -ForegroundColor Green
        } else {
            Write-Host "    ⚠ URL doesn't look like GitHub" -ForegroundColor Yellow
        }
    } else {
        Write-Host "    ✗ No remote configured" -ForegroundColor Red
        Write-Host "    Run: git remote add origin https://github.com/YOUR-USERNAME/REPO.git" -ForegroundColor Yellow
    }
} catch {
    Write-Host "    ✗ Cannot check remote" -ForegroundColor Red
}
Write-Host ""

# Check 7: Current branch
Write-Host "[7/8] Checking current branch..." -ForegroundColor Yellow
try {
    $branch = git branch --show-current 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "    Current branch: $branch" -ForegroundColor Gray
        if ($branch -eq "main" -or $branch -eq "master") {
            Write-Host "    ✓ On correct branch" -ForegroundColor Green
        } else {
            Write-Host "    ⚠ Unusual branch name" -ForegroundColor Yellow
        }
    }
} catch {
    Write-Host "    ✗ Cannot determine branch" -ForegroundColor Red
}
Write-Host ""

# Check 8: Recent commits
Write-Host "[8/8] Checking recent commits..." -ForegroundColor Yellow
try {
    $commits = git log --oneline -3 2>&1
    if ($LASTEXITCODE -eq 0 -and $commits) {
        Write-Host "    ✓ Recent commits found:" -ForegroundColor Green
        Write-Host $commits -ForegroundColor Gray
    } else {
        Write-Host "    ⚠ No commits found" -ForegroundColor Yellow
        Write-Host "    You need to commit your files first" -ForegroundColor Yellow
    }
} catch {
    Write-Host "    ✗ Cannot check commits" -ForegroundColor Red
}
Write-Host ""

# Summary
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host "SUMMARY & RECOMMENDATIONS" -ForegroundColor Cyan
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host ""

# Check if ready to push
$readyToPush = $true

if (-not (Test-Path ".git")) {
    Write-Host "❌ Git not initialized" -ForegroundColor Red
    Write-Host "   Action: git init" -ForegroundColor Yellow
    $readyToPush = $false
}

if ($missingFiles.Count -gt 0) {
    Write-Host "❌ Missing required files: $($missingFiles -join ', ')" -ForegroundColor Red
    $readyToPush = $false
}

try {
    $remotes = git remote -v 2>&1
    if (-not $remotes) {
        Write-Host "❌ No GitHub remote configured" -ForegroundColor Red
        Write-Host "   Action: git remote add origin YOUR_GITHUB_URL" -ForegroundColor Yellow
        $readyToPush = $false
    }
} catch {}

if ($readyToPush) {
    Write-Host "✓ Repository looks ready!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Next steps to push to GitHub:" -ForegroundColor Cyan
    Write-Host "1. git add -A" -ForegroundColor White
    Write-Host "2. git commit -m 'Complete project files'" -ForegroundColor White
    Write-Host "3. git push -u origin main" -ForegroundColor White
    Write-Host ""
    Write-Host "Then check GitHub URL and refresh (Ctrl+F5)" -ForegroundColor Cyan
} else {
    Write-Host "⚠ Issues detected - follow the actions above" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host "Need more help?" -ForegroundColor Cyan
Write-Host "See RAILWAY_DEPLOY.md section:" -ForegroundColor Cyan
Write-Host "'Step 3.1b: Troubleshooting - Files Not Showing in GitHub'" -ForegroundColor White
Write-Host "=====================================" -ForegroundColor Cyan
