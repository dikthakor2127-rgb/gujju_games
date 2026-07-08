# 🎮 Gujju Games - Multiplayer Gaming Platform

A fun and interactive web-based gaming platform built with Flask and MySQL. Play classic games, compete with other players, and climb the leaderboard!

## 🎯 Features

- **6 Playable Games**: Tic Tac Toe, Brick Breaker, Snake & Apple, Space Shooter, Flappy Bird, Car Racing
- **User Authentication**: Secure login and registration system
- **Live Dashboard**: Real-time stats and score updates
- **Leaderboard**: Global rankings with top players
- **Match History**: Track all your game results
- **Admin Panel**: Game and user management
- **Dark/Light/Auto Theme**: Customizable UI themes
- **Responsive Design**: Works on desktop and mobile devices

## 🚀 Deployment

### Option 1: Deploy to Heroku (Recommended)

#### Prerequisites:
- Heroku account ([Sign up here](https://www.heroku.com))
- Git installed
- GitHub account

#### Steps:

1. **Push code to GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit: Gujju Games deployment ready"
   git remote add origin https://github.com/YOUR_USERNAME/gujju-games.git
   git branch -M main
   git push -u origin main
   ```

2. **Create Heroku App**
   ```bash
   heroku login
   heroku create your-app-name
   ```

3. **Set Environment Variables**
   ```bash
   heroku config:set DB_HOST=your-db-host
   heroku config:set DB_USER=your-db-user
   heroku config:set DB_PASSWORD=your-db-password
   heroku config:set DB_NAME=your-db-name
   heroku config:set FLASK_SECRET_KEY=your-secret-key
   ```

4. **Deploy**
   ```bash
   git push heroku main
   ```

5. **View your app**
   ```bash
   heroku open
   ```

### Option 2: Deploy to Railway

#### Prerequisites:
- Railway account ([Sign up here](https://railway.app))
- GitHub repository

#### Steps:

1. Push code to GitHub (see steps above)
2. Go to [Railway.app](https://railway.app)
3. Click "New Project" → "Deploy from GitHub repo"
4. Select your `gujju-games` repository
5. Add environment variables in the Railway dashboard
6. Railway will auto-deploy on every push

### Option 3: Deploy to Render

#### Prerequisites:
- Render account ([Sign up here](https://render.com))
- GitHub repository

#### Steps:

1. Push code to GitHub
2. Go to [Render.com](https://render.com)
3. Click "New +" → "Web Service"
4. Connect your GitHub repository
5. Set build command: `pip install -r requirements.txt`
6. Set start command: `gunicorn app:app`
7. Add environment variables
8. Deploy

## 📦 Local Setup

### Prerequisites:
- Python 3.8+
- MySQL Server
- Git

### Installation:

1. **Clone the repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/gujju-games.git
   cd gujju-games
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your database credentials
   ```

5. **Create database**
   ```bash
   mysql -u root -p < gujju_games.sql
   ```

6. **Run the application**
   ```bash
   python app.py
   ```

7. **Access the app**
   - Open http://localhost:5000 in your browser

## 🎮 Games

### Tic Tac Toe
Classic strategy game. Outsmart your opponent and claim victory.

### Brick N Ball
Destroy every brick, survive longer, and push for the highest score.

### Snake & Apple
Collect apples, grow longer, and survive the endless challenge.

### Space Shooter
Defend the galaxy, destroy enemies, and achieve maximum score.

### Flappy Bird
Fly through endless pipes. Precision and timing are everything.

### Car Racing
Dodge obstacles, race at top speed, and set a record score.

## 🔐 Security Notes

- Never commit `.env` files with sensitive data
- Use strong `FLASK_SECRET_KEY` in production
- Keep database credentials secure
- Use HTTPS in production
- Update dependencies regularly

## 📁 Project Structure

```
gujju-games/
├── app.py                 # Main Flask application
├── db.py                  # Database connection
├── quiz.py               # Quiz functionality
├── requirements.txt      # Python dependencies
├── runtime.txt          # Python version
├── Procfile             # Deployment configuration
├── .env.example         # Environment variables template
├── .gitignore           # Git ignore rules
├── static/              # Static files (CSS, JS, images)
│   ├── css/
│   ├── js/
│   └── images/
├── templates/           # HTML templates
│   ├── dashboard.html
│   ├── login.html
│   ├── registration.html
│   └── ... (game templates)
└── README.md           # This file
```

## 🔗 Live Endpoints

- **Home**: `/`
- **Dashboard**: `/dashboard`
- **Registration**: `/registration`
- **Login**: `/login`
- **Profile**: `/profile`
- **Leaderboard**: `/leaderboard`
- **Match History**: `/history`
- **API - User Stats**: `/api/user-stats`
- **Save Score**: `/save-score` (POST)
- **Save History**: `/save_history` (POST)

## 🛠️ Tech Stack

- **Backend**: Flask (Python)
- **Database**: MySQL
- **Frontend**: HTML5, CSS3, JavaScript
- **Server**: Gunicorn
- **Deployment**: Heroku / Railway / Render
- **Version Control**: Git

## 👥 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see LICENSE file for details.

## 💬 Support

For issues, questions, or suggestions, please open an issue on GitHub or contact us.

---

**Made with ❤️ by Gujju Developers**
