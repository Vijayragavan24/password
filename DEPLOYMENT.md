# DEPLOYMENT GUIDE

## Production Deployment Checklist

### 1. Security Hardening

- [ ] Change `SECRET_KEY` to a strong random value
- [ ] Set `DEBUG = False` in configuration
- [ ] Use environment variables for all secrets
- [ ] Enable HTTPS/SSL certificates
- [ ] Set secure cookies: `SESSION_COOKIE_SECURE = True`
- [ ] Set SameSite cookies: `SESSION_COOKIE_SAMESITE = 'Lax'`
- [ ] Add CSRF validation to all forms
- [ ] Implement rate limiting on authentication endpoints
- [ ] Enable CORS only for trusted domains

### 2. Database Security

- [ ] Use strong, unique database password
- [ ] Enable database encryption
- [ ] Regular backup strategy implemented
- [ ] Database user with minimal required permissions
- [ ] Enable SSL for database connections

### 3. Performance

- [ ] Use production WSGI server (Gunicorn, uWSGI)
- [ ] Set up reverse proxy (Nginx)
- [ ] Enable gzip compression
- [ ] Minify CSS and JavaScript
- [ ] Implement caching strategy
- [ ] Use CDN for static assets
- [ ] Enable database query optimization
- [ ] Add monitoring and logging

### 4. Infrastructure

- [ ] Deploy on secured server
- [ ] Enable firewall rules
- [ ] Use environment variables from secure vault
- [ ] Configure automated backups
- [ ] Set up monitoring alerts
- [ ] Enable audit logging
- [ ] Regular security updates and patches

---

## Deployment with Gunicorn (Linux/macOS)

### 1. Install Gunicorn
```bash
pip install gunicorn
```

### 2. Create Systemd Service (Linux)
Create `/etc/systemd/system/password-detector.service`:
```ini
[Unit]
Description=Password Detection Tool
After=network.target

[Service]
User=www-data
WorkingDirectory=/path/to/Password Detection Tool
ExecStart=/path/to/venv/bin/gunicorn --workers 4 --bind 0.0.0.0:8000 app:app
Restart=always

[Install]
WantedBy=multi-user.target
```

### 3. Start Service
```bash
sudo systemctl start password-detector
sudo systemctl enable password-detector
```

---

## Deployment with Nginx

Create `/etc/nginx/sites-available/password-detector`:
```nginx
server {
    listen 80;
    server_name your-domain.com;

    client_max_body_size 20M;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static/ {
        alias /path/to/Password Detection Tool/static/;
        expires 30d;
    }
}
```

Enable the site:
```bash
sudo ln -s /etc/nginx/sites-available/password-detector /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

---

## SSL/TLS with Let's Encrypt

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

---

## Docker Deployment (Optional)

Create `Dockerfile`:
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV FLASK_APP=app.py
ENV FLASK_ENV=production

EXPOSE 5000

CMD ["gunicorn", "--workers", "4", "--bind", "0.0.0.0:5000", "app:app"]
```

Build and run:
```bash
docker build -t password-detector .
docker run -p 80:5000 -e SQLALCHEMY_DATABASE_URI=... password-detector
```

---

## Database Migration

For updating database schema in production:

```bash
# Create migration
flask db init
flask db migrate -m "description"
flask db upgrade
```

---

## Monitoring and Logging

### Enable Application Logging
```python
import logging

logging.basicConfig(
    filename='app.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)
```

### Monitor Metrics
- CPU usage
- Memory usage
- Database connections
- Request latency
- Error rates

---

## Backup Strategy

### Database Backups
```bash
# Full backup
mysqldump -u user -p password_detector > backup.sql

# Scheduled backup (Cron)
0 2 * * * mysqldump -u user -p database_name > /backup/db_$(date +\%Y\%m\%d).sql
```

### Restore from Backup
```bash
mysql -u user -p database_name < backup.sql
```

---

## Performance Tuning

### Database Optimization
```sql
-- Add indexes for frequently queried columns
CREATE INDEX idx_user_email ON users(email);
CREATE INDEX idx_password_user_id ON password_history(user_id);
CREATE INDEX idx_password_date ON password_history(date_checked);
```

### Application Optimization
- Enable query caching
- Use connection pooling
- Compress static assets
- Remove debug logging in production

---

## Security Testing

Before production deployment:

1. **Penetration Testing**
   - SQL Injection tests
   - XSS vulnerability tests
   - CSRF attack tests
   - Authentication bypass tests

2. **Load Testing**
   - Determine max concurrent users
   - Identify bottlenecks
   - Stress test the system

3. **Security Audit**
   - Code review
   - Dependency vulnerability scan
   - Configuration audit

---

## Maintenance

### Regular Tasks
- Monitor error logs daily
- Weekly database optimization
- Monthly security updates
- Quarterly backup verification
- Annual security audit

### Health Checks
```bash
# Check application status
curl http://localhost:5000/

# Check database connection
curl http://localhost:5000/api/statistics
```

---

## Rollback Procedure

In case of critical issues:

1. Identify the problematic version
2. Restore from previous backup
3. Revert code to stable version
4. Restart application
5. Run smoke tests
6. Monitor for errors

---

## Scaling Considerations

As traffic grows:

1. **Horizontal Scaling**
   - Add multiple application servers
   - Use load balancer (HAProxy, AWS ELB)
   - Share session data (Redis)

2. **Vertical Scaling**
   - Upgrade server resources
   - Optimize code and queries

3. **Caching Layer**
   - Implement Redis for sessions
   - Cache frequently accessed data
   - Cache API responses

4. **Database Scaling**
   - Read replicas
   - Database sharding
   - Connection pooling

---

## Disaster Recovery

- Regular backup testing
- Documented recovery procedures
- Redundant systems
- Failover mechanisms
- Business continuity plan

---

## Post-Deployment Monitoring

Monitor these metrics:
- Response time
- Error rate
- CPU/Memory usage
- Database query time
- User growth
- Security incidents

---

**Important**: Always test thoroughly in a staging environment before deploying to production.
