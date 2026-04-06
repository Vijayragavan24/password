# Password Strength and Breach Detection Tool

A modern, feature-rich web application for analyzing password strength, detecting breaches, and providing security recommendations.

## Features

- 🔐 **Real-time Password Analysis** - Instant strength checking with detailed metrics
- 🛡️ **Breach Detection** - Check if passwords have been found in data breaches
- 💡 **Security Recommendations** - Get actionable tips to improve password strength
- 📊 **Dashboard Analytics** - Track password history and security statistics
- 🎨 **Modern UI/UX** - Glassmorphism design with smooth animations
- 🔄 **Secure Authentication** - Bcrypt password hashing and session management
- 📝 **Security Questions** - Account recovery using security questions
- 🎯 **Password Generator** - Generate secure random passwords
- 📱 **Responsive Design** - Works seamlessly on all devices
- 📈 **Charts & Analytics** - Visual representation of password strength trends

## Technology Stack

- **Backend**: Python (Flask)
- **Frontend**: HTML5, CSS3, JavaScript
- **Database**: MySQL
- **UI Framework**: Bootstrap 5
- **Icons**: Font Awesome
- **Animations**: AOS (Animate On Scroll)
- **Charts**: Chart.js
- **Security**: Bcrypt, Session Management

## Project Structure

```
Password Detection Tool/
├── app.py                    # Main Flask application
├── models.py                 # Database models
├── requirements.txt          # Python dependencies
├── .env                      # Environment variables
├── README.md                 # This file
├── templates/                # HTML templates
│   ├── base.html
│   ├── welcome.html
│   ├── register.html
│   ├── login.html
│   ├── forgot_password.html
│   ├── security_verification.html
│   ├── reset_password.html
│   ├── dashboard.html
│   ├── password_tool.html
│   ├── profile.html
│   ├── 404.html
│   └── 500.html
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── main.js
└── docs/                     # Documentation (optional)
```

## Installation

### Prerequisites

- Python 3.8+
- MySQL Server
- Git

### Setup Instructions

1. **Clone or navigate to the project directory**
   ```bash
   cd "Password Detection Tool"
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Configure the database**
   
   Update the `.env` file with your MySQL credentials:
   ```
   SQLALCHEMY_DATABASE_URI=mysql+pymysql://username:password@localhost:3306/password_detector
   SECRET_KEY=your-secret-key-here
   ```

6. **Create the database**
   ```bash
   mysql -u root -p
   CREATE DATABASE password_detector;
   EXIT;
   ```

7. **Run the application**
   ```bash
   python app.py
   ```

8. **Access the application**
   Open your browser and navigate to: `http://localhost:5000`

## User Flow

### Welcome Page
- Landing page with project overview
- Call-to-action buttons for registration and login
- Features and security tips sections

### Registration
- Create account with username, email, password
- Set security questions (mother's name, date of birth, favorite color)
- Password strength meter
- Email validation

### Login
- Sign in with username or email
- Show/hide password toggle
- Remember me option
- Forgot password link

### Forgot Password Recovery
- Enter email or username
- Answer security questions
- Reset password with strength meter
- Validation and confirmation

### Dashboard
- User profile section
- Statistics cards (Total checked, Strong, Weak, Breached)
- Charts for password strength distribution
- Security status overview
- Quick action buttons

### Password Tool (Main Feature)
- Real-time password analysis
- Strength meter with detailed checks
- Security recommendations
- Password generator with customizable options
- Analysis history table
- Breach detection status

### Profile
- View account information
- Security question display
- Account creation and update dates
- Logout option

## Security Features

- **Password Hashing**: Bcrypt with salt for secure password storage
- **SQL Injection Protection**: SQLAlchemy ORM prevents SQL injection
- **CSRF Protection**: Flask-WTF prevents CSRF attacks
- **Session Management**: Secure session handling with Flask-Login
- **Input Validation**: Server-side validation for all user inputs
- **Password Strength Analysis**: 
  - Length requirements (8+ characters)
  - Character variety (uppercase, lowercase, numbers, special)
  - Common password detection
  - Pattern detection (repeated, sequential characters)

## Password Strength Algorithm

The password strength is calculated based on:
- **Length**: Bonus for 8+, 12+, and 16+ characters
- **Character Variety**: Points for uppercase, lowercase, numbers, special characters
- **Pattern Safety**: Deductions for repeated/sequential characters
- **Dictionary Checks**: Deductions for common passwords

Strength Levels:
- **Very Weak** (0-20%)
- **Weak** (20-40%)
- **Medium** (40-60%)
- **Strong** (60-80%)
- **Very Strong** (80-100%)

## API Endpoints

### Authentication
- `POST /register` - User registration
- `POST /login` - User login
- `GET /logout` - User logout

### Password Management
- `GET /forgot-password` - Forgot password page
- `POST /forgot-password` - Initiate password recovery
- `POST /security-verification` - Verify security answers
- `POST /reset-password` - Reset password

### Password Analysis
- `POST /api/analyze-password` - Analyze password strength
- `POST /api/generate-password` - Generate secure password
- `GET /api/password-history` - Get user's password check history
- `GET /api/statistics` - Get dashboard statistics

### User Management
- `GET /dashboard` - User dashboard
- `GET /password-tool` - Password analysis tool
- `GET /profile` - User profile
- `GET /api/user` - Get current user info

## Database Schema

### Users Table
```sql
CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(80) UNIQUE NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    mother_name VARCHAR(120) NOT NULL,
    date_of_birth VARCHAR(20) NOT NULL,
    favorite_color VARCHAR(50) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

### Password History Table
```sql
CREATE TABLE password_history (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    password_checked VARCHAR(255) NOT NULL,
    strength VARCHAR(20) NOT NULL,
    score INT DEFAULT 0,
    breach_status BOOLEAN DEFAULT FALSE,
    date_checked DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```

## Configuration

### Environment Variables (.env)
```
FLASK_ENV=development
FLASK_APP=app.py
SECRET_KEY=your-secret-key-change-in-production
SQLALCHEMY_DATABASE_URI=mysql+pymysql://user:password@localhost:3306/password_detector
DEBUG=True
```

## Advanced Features

### Current Implementation
- ✅ Real-time password strength analysis
- ✅ Security question-based password recovery
- ✅ Password history tracking
- ✅ Dashboard with statistics
- ✅ Password generator
- ✅ Breach detection simulation
- ✅ Responsive design
- ✅ Animated UI with AOS
- ✅ Chart.js analytics

### Future Enhancements
- [ ] Integration with Have I Been Pwned API for real breach detection
- [ ] Two-factor authentication (2FA)
- [ ] Dark mode toggle
- [ ] Export security reports as PDF
- [ ] Password strength comparison with trends
- [ ] Admin panel for user management
- [ ] Email verification for registration
- [ ] Social media login integration
- [ ] AI-powered password suggestions
- [ ] Multi-language support

## Troubleshooting

### Database Connection Error
- Ensure MySQL server is running
- Check credentials in `.env` file
- Verify database exists: `SHOW DATABASES;`

### Port Already in Use
- Change the port in `app.py`: `app.run(port=5001)`
- Or kill the process using port 5000

### Module Import Error
- Activate virtual environment
- Reinstall requirements: `pip install -r requirements.txt`

### Session Issues
- Clear browser cookies and cache
- Restart Flask application
- Check `SECRET_KEY` is properly set

## Performance Tips

- Use CDN for static assets in production
- Enable gzip compression
- Implement caching for frequently accessed data
- Use database indexing on frequently queried columns
- Minify CSS and JavaScript files

## Security Considerations

1. **Change SECRET_KEY** in production
2. **Use environment variables** for sensitive data
3. **Enable HTTPS** in production
4. **Set secure session cookies** in production
5. **Implement rate limiting** for authentication endpoints
6. **Regular security audits** of the codebase
7. **Keep dependencies updated** for security patches
8. **Use strong database passwords**
9. **Implement proper logging** for audit trails
10. **Regular database backups**

## License

This project is licensed under the MIT License. See LICENSE file for details.

## Contributing

Contributions are welcome! Please follow these steps:
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a pull request

## Support

For issues and questions:
- Create an issue on GitHub
- Check existing documentation
- Review the FAQ section

## Authors

- Development Team

## Changelog

### Version 1.0.0 (Initial Release)
- Complete password strength analyzer
- User authentication system
- Dashboard with analytics
- Password generator
- Security question-based recovery
- Responsive UI with animations

## Roadmap

- Q1 2024: Real breach API integration
- Q2 2024: 2FA implementation
- Q3 2024: Dark mode and UI improvements
- Q4 2024: Admin panel and analytics

---

**Last Updated**: 2024
**Status**: Production Ready
