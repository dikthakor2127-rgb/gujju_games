# Contributing to Gujju Games

Thank you for your interest in contributing to Gujju Games! This document provides guidelines and instructions for contributing.

## Code of Conduct

- Be respectful and inclusive
- No harassment, discrimination, or abusive behavior
- Focus on constructive feedback
- Help others learn and grow

## Getting Started

### 1. Fork the Repository
```bash
# Click "Fork" button on GitHub
```

### 2. Clone Your Fork
```bash
git clone https://github.com/YOUR_USERNAME/gujju-games.git
cd gujju-games
```

### 3. Create Feature Branch
```bash
git checkout -b feature/your-feature-name
```

### 4. Set Up Development Environment
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy .env.example to .env
cp .env.example .env
# Edit .env with your database credentials

# Create database
mysql -u root -p < gujju_games.sql

# Run application
python app.py
```

## Development Guidelines

### Code Style
- Follow PEP 8 Python style guide
- Use meaningful variable and function names
- Add comments for complex logic
- Keep functions small and focused

### File Structure
```
- Backend: app.py, db.py
- Frontend: templates/, static/
- Configuration: requirements.txt, .env.example
- Tests: test_* files
```

### Database Changes
- Document any schema changes
- Create migration files if needed
- Test with fresh database

### Frontend Development
- Use semantic HTML
- Keep CSS organized and documented
- Test on different screen sizes
- Ensure accessibility (WCAG 2.1)

## Making Changes

### 1. Make Your Changes
```bash
# Edit files
git add .
git commit -m "feat: add your feature description"
```

### 2. Follow Commit Message Format
```
type: subject

body (optional)
footer (optional)

Types:
- feat: New feature
- fix: Bug fix
- refactor: Code refactoring
- docs: Documentation changes
- style: Code style changes
- test: Adding/updating tests
- chore: Maintenance tasks
```

### 3. Test Your Changes
```bash
# Run the application locally
python app.py

# Test all features affected by your changes
# Test on different browsers/devices
```

### 4. Push to Your Fork
```bash
git push origin feature/your-feature-name
```

### 5. Create Pull Request
- Go to GitHub
- Click "Compare & pull request"
- Fill out PR template
- Link related issues
- Provide clear description

## Pull Request Guidelines

### PR Title Format
```
[type] Short description (50 chars max)

Examples:
[feat] Add multiplayer game mode
[fix] Fix leaderboard sorting bug
[docs] Update deployment guide
```

### PR Description Should Include
- What changes were made
- Why the changes were necessary
- How to test the changes
- Any breaking changes
- Screenshots for UI changes

### PR Checklist
- [ ] Code follows style guidelines
- [ ] Self-reviewed changes
- [ ] Comments added for complex logic
- [ ] Documentation updated
- [ ] No new warnings generated
- [ ] Tests pass locally
- [ ] Database compatible

## Adding New Features

### New Game Template
1. Create game template in `templates/`
2. Add game logic in `static/js/`
3. Add styling in `static/css/`
4. Create Flask route in `app.py`
5. Add images in `static/images/`
6. Update dashboard with new game
7. Update leaderboard logic

### New API Endpoint
1. Add route to `app.py`
2. Add documentation in code
3. Handle error cases
4. Return appropriate status codes
5. Test with curl/Postman
6. Update README.md

### Database Changes
1. Update `gujju_games.sql`
2. Add migration if needed
3. Update `db.py` if needed
4. Document schema changes

## Testing

### Local Testing
```bash
# Test user registration
# Test user login
# Test each game
# Test leaderboard
# Test admin features
# Test mobile responsiveness
```

### Browser Testing
- Chrome/Edge (Chromium)
- Firefox
- Safari
- Mobile browsers

## Documentation

### Update These Files
- `README.md` - Feature overview
- `DEPLOYMENT_GUIDE.md` - Deployment changes
- Code comments - Complex logic
- Docstrings - Functions/classes

## Reporting Issues

### Before Creating Issue
- [ ] Check existing issues
- [ ] Search closed issues
- [ ] Test with latest code

### Issue Template
```markdown
**Describe the bug**
Clear description of the issue

**Steps to reproduce**
1. Go to...
2. Click...
3. See error

**Expected behavior**
What should happen

**Screenshots**
If applicable

**Environment**
- OS: Windows 10
- Browser: Chrome 100
- Python version: 3.11
```

## Review Process

### What Reviewers Look For
- Code quality and style
- Functionality and logic
- Performance impact
- Security issues
- Documentation completeness
- Test coverage

### Responding to Feedback
- Respond promptly
- Ask for clarification if needed
- Make requested changes
- Push updates to your branch
- Request re-review

## Code Review Checklist

- [ ] Follows project style
- [ ] No duplicate code
- [ ] Error handling present
- [ ] Comments are clear
- [ ] No hardcoded values
- [ ] Security best practices
- [ ] Database queries optimized
- [ ] Frontend is responsive

## Getting Help

- **Discord**: [Link to server]
- **Issues**: Open a GitHub issue
- **Discussions**: Use GitHub Discussions
- **Email**: [contact email]

## Recognition

Contributors will be:
- Added to CONTRIBUTORS.md
- Mentioned in releases
- Credited in pull request

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

**Thank you for contributing to Gujju Games! 🎮❤️**
