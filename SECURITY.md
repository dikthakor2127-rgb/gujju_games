# Security Policy

## Reporting Security Vulnerabilities

**Please DO NOT create a public GitHub issue for security vulnerabilities.**

Instead, email security details to: **security@gujjugames.com**

Include:
- Description of vulnerability
- Steps to reproduce
- Potential impact
- Suggested fix (if any)

We will respond within 48 hours.

## Security Best Practices

### 1. Environment Variables
- ✅ Store sensitive data in `.env` files
- ✅ Use strong `FLASK_SECRET_KEY`
- ✅ Never commit `.env` to version control
- ✅ Use unique keys for each environment

### 2. Database Security
- ✅ Use strong database passwords
- ✅ Limit database user permissions
- ✅ Use SSL connections to database
- ✅ Regular database backups
- ✅ Never hardcode credentials

### 3. Authentication
- ✅ Hash passwords with `werkzeug.security`
- ✅ Implement CSRF protection
- ✅ Use secure session cookies
- ✅ Implement rate limiting on login
- ✅ Add 2FA when possible

### 4. API Security
- ✅ Validate all inputs
- ✅ Sanitize outputs
- ✅ Use HTTPS only
- ✅ Implement CORS properly
- ✅ Add API rate limiting

### 5. Frontend Security
- ✅ Use Content Security Policy (CSP)
- ✅ Sanitize HTML output
- ✅ Validate client-side inputs
- ✅ Use secure cookies (HttpOnly, Secure flags)
- ✅ Keep JavaScript dependencies updated

### 6. Deployment Security
- ✅ Use HTTPS/TLS everywhere
- ✅ Enable HSTS headers
- ✅ Keep dependencies updated
- ✅ Use security headers
- ✅ Enable logging and monitoring

### 7. Code Security
```python
# ✅ Good: Use parameterized queries
cursor.execute(
    "SELECT * FROM users WHERE username=%s",
    (username,)
)

# ❌ Bad: String concatenation (SQL Injection)
cursor.execute(f"SELECT * FROM users WHERE username='{username}'")

# ✅ Good: Hash passwords
from werkzeug.security import generate_password_hash
hashed = generate_password_hash(password)

# ❌ Bad: Store plain text passwords
user.password = password
```

### 8. Error Handling
```python
# ✅ Good: Generic error messages
return "Login failed", 401

# ❌ Bad: Leaking information
return f"User '{username}' not found"
```

## Security Headers

Add these to production deployment:

```
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
X-XSS-Protection: 1; mode=block
Strict-Transport-Security: max-age=31536000; includeSubDomains
Content-Security-Policy: default-src 'self'
```

## Dependency Security

```bash
# Check for vulnerable packages
pip-audit

# Update packages safely
pip install --upgrade pip
pip install -U -r requirements.txt

# Verify package integrity
pip install --require-hashes -r requirements.txt
```

## Regular Security Checks

- [ ] Review recent commits for secrets
- [ ] Check dependency vulnerabilities
- [ ] Test authentication flows
- [ ] Review database permissions
- [ ] Check for hardcoded values
- [ ] Verify HTTPS is enforced
- [ ] Test input validation
- [ ] Review error messages

## Security Compliance

### OWASP Top 10 Considerations

1. **Injection** - Use parameterized queries
2. **Broken Auth** - Implement proper authentication
3. **Sensitive Data** - Encrypt and hash appropriately
4. **XML/XXE** - Validate XML inputs
5. **Broken Access Control** - Check permissions
6. **Security Misconfiguration** - Use security headers
7. **XSS** - Sanitize outputs
8. **Insecure Deserialization** - Avoid unsafe unserialize
9. **Using Components with Known Vulnerabilities** - Keep updated
10. **Insufficient Logging** - Log security events

## Incident Response

If a security issue is discovered:

1. **Immediately patch** the vulnerability
2. **Notify users** if data exposed
3. **Document** what happened
4. **Implement fixes** and test thoroughly
5. **Update** deployment
6. **Monitor** for exploitation

## Support

For security questions or concerns:
- Email: security@gujjugames.com
- Create confidential issue on GitHub
- Contact repository maintainers

---

**Security is everyone's responsibility. Thank you for helping keep Gujju Games safe! 🔒**
