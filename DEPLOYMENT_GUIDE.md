# 🚀 Deployment Guide - Gujju Games

Complete step-by-step guides for deploying Gujju Games to different platforms.

---

## 📋 Prerequisites (All Platforms)

1. **GitHub Account** - [Sign up](https://github.com)
2. **Git installed** - [Download](https://git-scm.com/download)
3. **Repository created** on GitHub

### Initial GitHub Setup

```bash
# Initialize git in your project
git init

# Add all files
git add .

# Create initial commit
git commit -m "Initial commit: Gujju Games deployment ready"

# Add remote repository
git remote add origin https://github.com/YOUR_USERNAME/gujju-games.git

# Set main branch
git branch -M main

# Push to GitHub
git push -u origin main
```

---

## ☁️ Option 1: Heroku Deployment (Recommended for Beginners)

### Pros:
- ✅ Easy setup and deployment
- ✅ Free tier available
- ✅ Automatic scaling
- ✅ Built-in GitHub integration

### Cons:
- ❌ Free tier dyno sleeps after inactivity
- ❌ Limited database options on free tier
- ❌ Requires credit card for better uptime

### Step-by-Step Setup:

#### 1. Create Heroku Account
- Go to [heroku.com](https://www.heroku.com)
- Sign up for free account
- Verify email

#### 2. Install Heroku CLI
```bash
# Windows (using Chocolatey)
choco install heroku-cli

# Or download from: https://devcenter.heroku.com/articles/heroku-cli
```

#### 3. Login to Heroku
```bash
heroku login
# Browser will open for authentication
```

#### 4. Create Heroku App
```bash
# Replace "gujju-games-prod" with your desired app name
heroku create gujju-games-prod

# Verify it was created
heroku apps
```

#### 5. Set Environment Variables
```bash
heroku config:set DB_HOST=your-database-host
heroku config:set DB_USER=your-database-user
heroku config:set DB_PASSWORD=your-secure-password
heroku config:set DB_NAME=gujju_games
heroku config:set FLASK_SECRET_KEY=your-super-secret-key-change-this
heroku config:set FLASK_ENV=production

# Verify variables are set
heroku config
```

#### 6. Deploy to Heroku
```bash
# Deploy using Git
git push heroku main

# View logs
heroku logs --tail

# Open app in browser
heroku open
```

#### 7. Configure Database (External)

For production, use a managed MySQL service:

**Option A: ClearDB (MySQL Provider)**
```bash
heroku addons:create cleardb:ignite
```

**Option B: JawsDB**
```bash
heroku addons:create jawsdb:kitefin
```

Then update your `DB_HOST`, `DB_USER`, `DB_PASSWORD` with the credentials provided.

### Useful Heroku Commands
```bash
# View logs
heroku logs --tail

# Restart dyno
heroku restart

# Run migrations/setup
heroku run python -c "from db import get_db_connection; print('DB connected')"

# View environment variables
heroku config

# Update code
git push heroku main

# Delete app
heroku apps:destroy --app gujju-games-prod
```

---

## 🚀 Option 2: Railway.app (Fastest Deploy)

### Pros:
- ✅ Super fast deployment
- ✅ GitHub integration (auto-deploy on push)
- ✅ Better free tier
- ✅ Built-in PostgreSQL/MySQL support
- ✅ Easy environment variable management

### Cons:
- ❌ Less documentation than Heroku
- ❌ Smaller community

### Step-by-Step Setup:

#### 1. Create Railway Account
- Go to [railway.app](https://railway.app)
- Sign up with GitHub
- Authorize Railway

#### 2. Create New Project
- Click **"New Project"**
- Select **"Deploy from GitHub Repo"**
- Authorize and select your `gujju-games` repository

#### 3. Add MySQL Database (Optional)
- In Railway dashboard, click **"+ New"**
- Select **"MySQL"**
- Railway will automatically create database with credentials

#### 4. Set Environment Variables
- Click on your web service
- Go to **Variables** tab
- Add:
  ```
  DB_HOST=mysql-container-name
  DB_USER=root
  DB_PASSWORD=generated-password
  DB_NAME=gujju_games
  FLASK_SECRET_KEY=your-secret-key
  FLASK_ENV=production
  ```

#### 5. Auto Deploy
- Every push to GitHub main branch auto-deploys!
- View logs in Railway dashboard
- Check deployment status

### Railway.app Dashboard Tips
```
Dashboard → Your Project → Deployments → View logs
Variables tab → Add/Edit environment variables
Settings → Custom domain setup
```

---

## 🎯 Option 3: Render.com

### Pros:
- ✅ Free tier with no sleep
- ✅ Native support for multiple databases
- ✅ Easy GitHub integration
- ✅ Auto-deploy on push
- ✅ Built-in SSL/HTTPS

### Cons:
- ❌ Cold starts on free tier
- ❌ Limited bandwidth

### Step-by-Step Setup:

#### 1. Create Render Account
- Go to [render.com](https://render.com)
- Sign up with GitHub
- Authorize Render

#### 2. Create Web Service
- Dashboard → **"New +"** → **"Web Service"**
- Connect your GitHub repository
- Select `gujju-games` repo

#### 3. Configure Service
- **Name**: gujju-games
- **Region**: Choose closest to you
- **Branch**: main
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `gunicorn app:app`
- **Plan**: Free

#### 4. Add Environment Variables
- Go to **Environment** section
- Add variables:
  ```
  DB_HOST=your-mysql-host
  DB_USER=root
  DB_PASSWORD=password
  DB_NAME=gujju_games
  FLASK_SECRET_KEY=your-secret-key
  FLASK_ENV=production
  ```

#### 5. Add MySQL Database
- Dashboard → **"New +"** → **"MySQL"**
- Same region as web service
- Note down credentials
- Update environment variables

#### 6. Deploy
- Click **"Create Web Service"**
- Render auto-deploys and provides URL
- View logs in dashboard

---

## 🐳 Option 4: Docker Deployment (Advanced)

Deploy using Docker containers to any cloud provider.

### Create Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV FLASK_ENV=production
ENV PORT=5000

EXPOSE 5000

CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:5000"]
```

### Create docker-compose.yml

```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "5000:5000"
    environment:
      DB_HOST: db
      DB_USER: root
      DB_PASSWORD: rootpassword
      DB_NAME: gujju_games
    depends_on:
      - db

  db:
    image: mysql:8
    environment:
      MYSQL_ROOT_PASSWORD: rootpassword
      MYSQL_DATABASE: gujju_games
    volumes:
      - ./gujju_games.sql:/docker-entrypoint-initdb.d/init.sql
      - mysql_data:/var/lib/mysql

volumes:
  mysql_data:
```

### Run Locally with Docker
```bash
docker-compose up -d
# App runs on http://localhost:5000
```

### Deploy to Docker Hub
```bash
docker build -t your-username/gujju-games .
docker push your-username/gujju-games
```

---

## 📊 Database Setup for Production

### Using External MySQL Services:

#### ClearDB
```
Provider: ClearDB MySQL
Credentials: Available in connection string
Integration: Heroku Add-ons
```

#### AWS RDS
```
1. Go to AWS RDS Console
2. Create MySQL instance
3. Note endpoint, username, password
4. Add credentials to environment variables
5. Import gujju_games.sql
```

#### DigitalOcean Managed Database
```
1. Create managed MySQL cluster
2. Add trusted sources (your app IP)
3. Import gujju_games.sql
4. Update environment variables
```

---

## ✅ Post-Deployment Checklist

- [ ] Database is connected and accessible
- [ ] All environment variables are set
- [ ] HTTPS/SSL is enabled
- [ ] Admin account is created
- [ ] Email notifications work (if applicable)
- [ ] Logs are being generated
- [ ] Backup strategy is in place
- [ ] CDN is configured (if needed)
- [ ] Monitoring/alerts are set up

---

## 🔍 Troubleshooting

### App Won't Start
```bash
# Check logs
heroku logs --tail          # Heroku
railway logs --follow       # Railway
# or check Render dashboard logs
```

### Database Connection Error
- Verify credentials are correct
- Check if database host is whitelisted
- Ensure database user has correct permissions
- Test connection locally first

### 502 Bad Gateway
- Check app logs for Python errors
- Restart the service
- Verify all dependencies in requirements.txt

### Performance Issues
- Use database indexing
- Add caching
- Optimize queries
- Increase server resources (if on paid tier)

---

## 📈 Scaling Tips

1. **Database**: Upgrade to managed service with replication
2. **Static Files**: Use CDN (Cloudflare, AWS CloudFront)
3. **Caching**: Implement Redis for session storage
4. **Load Balancing**: Use service-level load balancers
5. **Monitoring**: Set up error tracking (Sentry)

---

## 📞 Support

For deployment issues:
1. Check service documentation
2. Review application logs
3. Open GitHub issue with error details
4. Contact platform support

**Happy deploying! 🚀**
