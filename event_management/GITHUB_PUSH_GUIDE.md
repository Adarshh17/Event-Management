# Git Push to GitHub - Step by Step Guide

## Prerequisites
1. You have a GitHub account
2. Git is installed on your computer (download from: https://git-scm.com/)

---

## Step 1: Create a New Repository on GitHub

1. Go to https://github.com/
2. Click the **"+"** icon in the top right
3. Select **"New repository"**
4. Name it: `event-management-api` (or any name you prefer)
5. **Do NOT** initialize with README (we already have one)
6. Click **"Create repository"**
7. **Copy the repository URL** (looks like: `https://github.com/YOUR_USERNAME/event-management-api.git`)

---

## Step 2: Run These Commands in PowerShell

Open PowerShell in the project folder (`D:\new\event_management`) and run:

### Initialize Git (if not already done)
```powershell
cd D:\new\event_management
git init
```

### Configure Git (first time only)
```powershell
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

### Add All Files
```powershell
git add .
```

### Commit Files
```powershell
git commit -m "Initial commit: Event Management System API"
```

### Add Remote Repository
Replace `YOUR_USERNAME` with your actual GitHub username:
```powershell
git remote add origin https://github.com/YOUR_USERNAME/event-management-api.git
```

### Push to GitHub
```powershell
git branch -M main
git push -u origin main
```

---

## Step 3: Enter Credentials

When prompted:
- **Username**: Your GitHub username
- **Password**: Use a **Personal Access Token** (not your password)

### How to Create Personal Access Token:
1. Go to GitHub → Settings → Developer settings
2. Click "Personal access tokens" → "Tokens (classic)"
3. Click "Generate new token" → "Generate new token (classic)"
4. Give it a name (e.g., "Event Management API")
5. Select scopes: Check **"repo"** (full control of private repositories)
6. Click "Generate token"
7. **Copy the token** (you won't see it again!)
8. Use this token as your password when pushing

---

## Alternative: Using GitHub Desktop (Easier)

1. Download GitHub Desktop: https://desktop.github.com/
2. Install and sign in with your GitHub account
3. Click "File" → "Add Local Repository"
4. Select `D:\new\event_management`
5. Click "Publish repository"
6. Choose repository name and click "Publish"

Done! ✅

---

## Quick Copy-Paste Commands

**Replace `YOUR_USERNAME` with your GitHub username:**

```powershell
cd D:\new\event_management
git init
git add .
git commit -m "Initial commit: Event Management System API"
git remote add origin https://github.com/YOUR_USERNAME/event-management-api.git
git branch -M main
git push -u origin main
```

---

## Troubleshooting

### Error: "Git is not recognized"
- Install Git from: https://git-scm.com/
- Restart PowerShell after installation

### Error: "Authentication failed"
- Use Personal Access Token instead of password
- See instructions above for creating token

### Error: "Remote origin already exists"
- Run: `git remote remove origin`
- Then add it again

### Error: "Permission denied"
- Check your token has "repo" permissions
- Generate a new token if needed

---

## After Pushing Successfully

Your repository will be at:
```
https://github.com/YOUR_USERNAME/event-management-api
```

You can share this link with anyone! 🎉

---

## Update Repository Later

When you make changes:
```powershell
git add .
git commit -m "Description of changes"
git push
```

---

**Ready? Start with Step 1 above!** 🚀
