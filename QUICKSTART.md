# Quick Start Guide for Password Detection Tool

## Windows Users

### 1. Open Command Prompt or PowerShell
Navigate to the project directory:
```
cd "Path\to\Password Detection Tool"
```

### 2. Create Virtual Environment
```
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies
```
pip install -r requirements.txt
```

### 4. Configure MySQL Database
If you don't have MySQL installed, download and install it from: https://dev.mysql.com/downloads/mysql/

Then:
```
mysql -u root -p
CREATE DATABASE password_detector;
EXIT;
```

### 5. Update .env File
Edit the `.env` file with your MySQL credentials:
```
SQLALCHEMY_DATABASE_URI=mysql+pymysql://root:your_password@localhost:3306/password_detector
SECRET_KEY=your-secure-secret-key
```

### 6. Initialize Database
```
python setup.py
```

Or manually:
```
python -c "from app import app, db; app.app_context().push(); db.create_all()"
```

### 7. Run the Application
```
python app.py
```

### 8. Open in Browser
Visit: http://localhost:5000

---

## macOS/Linux Users

### 1. Open Terminal
Navigate to the project directory:
```
cd "Path/to/Password Detection Tool"
```

### 2. Create Virtual Environment
```
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```
pip install -r requirements.txt
```

### 4. Configure MySQL Database
Install MySQL if not already installed:
```
# macOS with Homebrew
brew install mysql

# Start MySQL
brew services start mysql

# Login
mysql -u root
```

Then:
```
CREATE DATABASE password_detector;
EXIT;
```

### 5. Update .env File
```
SQLALCHEMY_DATABASE_URI=mysql+pymysql://root:your_password@localhost:3306/password_detector
SECRET_KEY=your-secure-secret-key
```

### 6. Initialize Database
```
python setup.py
```

### 7. Run the Application
```
python app.py
```

### 8. Open in Browser
Visit: http://localhost:5000

---

## Test Account

You can create a test account using the registration page, or use these test credentials:

**Username**: testuser
**Email**: test@example.com
**Password**: TestPassword123!
**Mother's Name**: Test
**Date of Birth**: 1990-01-01
**Favorite Color**: Blue

---

## Troubleshooting

### Issue: Module Not Found
**Solution**: Make sure virtual environment is activated and all dependencies are installed.
```
pip install -r requirements.txt
```

### Issue: Database Connection Error
**Solution**: Check MySQL is running and credentials in .env are correct.
```
# Test MySQL connection
mysql -u root -p -e "SHOW DATABASES;"
```

### Issue: Port 5000 Already in Use
**Solution**: Change the port in app.py:
```python
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
```

### Issue: Template Not Found
**Solution**: Make sure you're running the app from the project root directory where templates/ folder exists.

### Issue: Static Files Not Loading
**Solution**: Clear browser cache (Ctrl+Shift+Delete) or use incognito mode.

---

## Features to Try

1. **Register a New Account**
   - Go to /register
   - Fill in all required fields
   - Answer security questions

2. **Test Password Strength Checker**
   - Login to your account
   - Go to /password-tool
   - Enter various passwords to see strength analysis

3. **Generate Secure Password**
   - In password tool, adjust generator settings
   - Generate a new password

4. **View Dashboard**
   - Check your statistics
   - View password history
   - See security charts

5. **Test Password Recovery**
   - Go to /forgot-password
   - Enter your username/email
   - Answer security questions
   - Reset your password

---

## Default Port and URL

- **URL**: http://localhost:5000
- **Port**: 5000 (configurable in app.py)
- **Debug Mode**: Enabled by default (disable in production)

---

## Project Structure Overview

```
Password Detection Tool/
├── app.py              # Main Flask application
├── models.py           # Database models
├── setup.py            # Setup wizard
├── requirements.txt    # Dependencies
├── .env               # Configuration
├── templates/         # HTML templates
│   └── [10+ HTML pages]
├── static/
│   ├── css/style.css  # Styling
│   └── js/main.js     # JavaScript utilities
└── README.md          # Full documentation
```

---

## Security Notes

⚠️ **Important for Production**:

1. Change `SECRET_KEY` in .env to a strong random value
2. Use environment variables for all sensitive data
3. Enable HTTPS
4. Disable DEBUG mode
5. Use strong database password
6. Implement rate limiting
7. Regular security audits
8. Keep dependencies updated

---

## Performance Optimization

- Use a production WSGI server (Gunicorn, uWSGI)
- Enable caching
- Use CDN for static assets
- Optimize database queries
- Minify CSS/JS files

---

## Support

For issues:
1. Check README.md for detailed documentation
2. Review error messages in console
3. Check MySQL is running
4. Verify .env configuration
5. Clear browser cache

---

**Version**: 1.0.0
**Last Updated**: 2024
**Status**: Production Ready
