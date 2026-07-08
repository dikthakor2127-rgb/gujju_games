# 🚀 Quick Start Guide

Get Gujju Games up and running in 5 minutes!

## 📋 Requirements

- Python 3.8+
- MySQL Server
- Git
- 5 minutes ⏱️

## ⚡ 1-Minute Local Setup

```bash
# Clone repository
git clone https://github.com/YOUR_USERNAME/gujju-games.git
cd gujju-games

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Setup database
mysql -u root -p < gujju_games.sql

# Run app
python app.py
```

✅ **App is running at http://localhost:5000**

## 🔧 Configuration

### 1. Create `.env` file
```bash
cp .env.example .env
```

### 2. Edit `.env` with your details
```env
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=gujju_games
FLASK_SECRET_KEY=your-super-secret-key
```

### 3. (Optional) Configure MySQL
```bash
# If MySQL isn't running
mysql.server start  # macOS
# or
mysqld              # Windows (in MySQL bin folder)
```

## 🎮 Quick Test

1. Open http://localhost:5000
2. Click **Register** → Create account
3. Click **Login** → Login with your credentials
4. Play a game! 🎯
5. Check **Leaderboard** → See your score

## 📱 Using Docker (Optional)

```bash
# Start with Docker
docker-compose up -d

# App runs at http://localhost:5000
# Database automatically initialized

# Stop
docker-compose down
```

## 🌐 Deploy to Internet (Choose One)

### A. Heroku (Easiest)
```bash
# Install Heroku CLI, then:
heroku login
heroku create your-app-name
heroku config:set DB_HOST=...
git push heroku main
heroku open
```

### B. Railway (Fastest)
- Go to railway.app
- Connect GitHub
- Select this repo
- Auto-deploys on push!

### C. Render (Free Tier)
- Go to render.com
- Select "Deploy from GitHub"
- Set build command: `pip install -r requirements.txt`
- Set start command: `gunicorn app:app`
- Auto-deploys!

## 📚 Learn More

- [Full Deployment Guide](DEPLOYMENT_GUIDE.md) - Detailed deployment steps
- [README](README.md) - Project overview
- [Contributing Guide](CONTRIBUTING.md) - How to contribute
- [Security Policy](SECURITY.md) - Security guidelines

## 🆘 Troubleshooting

### Port 5000 Already in Use
```bash
# Change port
python app.py --port 5001
```

### Database Connection Error
```bash
# Check MySQL is running
mysql -u root -p
# In MySQL: SELECT 1;
# Should return: 1

# Update .env with correct credentials
# Make sure DB exists:
# CREATE DATABASE gujju_games;
```

### Dependency Issues
```bash
# Reinstall dependencies
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

### Reset Database
```bash
# Drop and recreate
mysql -u root -p < gujju_games.sql
```

## 🎯 Next Steps

1. ✅ **Run locally** - Test all games
2. ✅ **Deploy** - Put it online
3. ✅ **Customize** - Change colors, games, content
4. ✅ **Contribute** - Add new features
5. ✅ **Share** - Tell others!

## 🔑 Default Admin Account

```
Username: admin
Password: Check admin creation in database
```

Create admin user:
```sql
INSERT INTO admins (Username, Password) 
VALUES ('admin', 'admin123');
```

## 📞 Need Help?

- Check [Troubleshooting](#troubleshooting)
- Read [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)
- Open GitHub Issue
- Check existing discussions

## 🎮 Games Included

1. **Tic Tac Toe** - Strategy game
2. **Brick N Ball** - Breakout style
3. **Snake & Apple** - Classic
4. **Space Shooter** - Action
5. **Flappy Bird** - Casual
6. **Car Racing** - Racing

## 🏆 Features

- ✅ Real-time leaderboard
- ✅ User authentication
- ✅ Match history
- ✅ Admin panel
- ✅ Dark/Light theme
- ✅ Responsive design
- ✅ Live stats

## 🚀 Deploy Now!

```bash
# Push to GitHub
git add .
git commit -m "Ready to deploy!"
git push origin main

# Then deploy to Heroku/Railway/Render
# (See deployment guide above)
```

**You're all set! Happy gaming! 🎉**

---

**Need a complete deployment walkthrough?** → See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)

**Want to contribute?** → See [CONTRIBUTING.md](CONTRIBUTING.md)

**Security questions?** → See [SECURITY.md](SECURITY.md)
