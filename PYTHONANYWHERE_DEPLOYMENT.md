# 🚀 PythonAnywhere Deployment Guide

## Step 1: Create PythonAnywhere Account
1. Go to [pythonanywhere.com](https://www.pythonanywhere.com)
2. Sign up for a free account (Beginner plan)
3. Verify your email

## Step 2: Upload Your Project
### Option A: Upload via Web Interface
1. Go to **Files** tab in PythonAnywhere
2. Click **Upload a file**
3. Upload all files from your project (except `venv/` folder)
4. Or use **Open bash console** and run:
```bash
# Clone from GitHub (recommended)
git clone https://github.com/yourusername/password-detection-tool.git
cd password-detection-tool
```

### Option B: Upload via Git (Recommended)
1. First, push your code to GitHub
2. In PythonAnywhere bash console:
```bash
git clone https://github.com/yourusername/password-detection-tool.git
cd password-detection-tool
```

## Step 3: Set Up Virtual Environment
```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install requirements
pip install -r requirements.txt
```

## Step 4: Configure Environment Variables
```bash
# Copy production environment file
cp .env.production .env

# Edit the .env file with your settings
nano .env
```

**Important:** Update these values in `.env`:
- `SECRET_KEY`: Generate a strong random key
- Email settings (optional but recommended for contact form)

## Step 5: Set Up Database
```bash
# Activate virtual environment
source venv/bin/activate

# Create database tables
python -c "
from app import app, db
with app.app_context():
    db.create_all()
    print('Database created successfully!')
"
```

## Step 6: Create Web App
1. Go to **Web** tab in PythonAnywhere
2. Click **Add a new web app**
3. Choose **Flask** and **Python 3.10**
4. Set the app path to: `/home/yourusername/password-detection-tool`
5. Set the app filename to: `app.py`

## Step 7: Configure WSGI File
PythonAnywhere will create a WSGI file. Edit it to look like this:

```python
# /var/www/yourusername_pythonanywhere_com_wsgi.py
import sys
import os

# Add your project directory to the path
project_home = '/home/yourusername/password-detection-tool'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Set environment variable to tell app we're in production
os.environ['FLASK_ENV'] = 'production'

# Import the Flask app
from app import app as application
```

## Step 8: Set Environment Variables
In PythonAnywhere **Web** tab:
1. Go to **Environment variables** section
2. Add: `FLASK_ENV = production`
3. Add your other environment variables from `.env` file

## Step 9: Reload Web App
1. Go back to **Web** tab
2. Click **Reload** button
3. Your app should now be live at: `https://yourusername.pythonanywhere.com`

## Step 10: Test Your App
- Visit your site: `https://yourusername.pythonanywhere.com`
- Test registration, login, password analysis
- Check dashboard and all features

## Troubleshooting

### Common Issues:

**1. Import Errors:**
```bash
# Make sure virtual environment is activated
source venv/bin/activate
pip install -r requirements.txt
```

**2. Database Issues:**
```bash
# Recreate database
python -c "
from app import app, db
with app.app_context():
    db.create_all()
"
```

**3. Static Files Not Loading:**
- Make sure static files are in `/static/` folder
- Check file permissions: `chmod 644 static/*`

**4. 500 Error:**
- Check logs in **Web** tab → **Error log**
- Make sure all environment variables are set

## Security Checklist
- ✅ Change `SECRET_KEY` to a strong random value
- ✅ Set `FLASK_ENV=production`
- ✅ Use HTTPS (PythonAnywhere provides free SSL)
- ✅ Set strong passwords for email accounts
- ✅ Regularly update dependencies

## Free Tier Limitations
- 512MB storage
- Limited CPU time
- No custom domains (use `yourusername.pythonanywhere.com`)

## Upgrading to Paid Plan
If you need more resources, consider upgrading to a paid plan for:
- More storage
- Custom domains
- More CPU time
- Priority support

---
**🎉 Your Password Detection Tool is now live on the internet!**