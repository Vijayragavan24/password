import os
from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_mail import Mail, Message
from datetime import datetime, timedelta
import bcrypt
import re
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-this')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI', 'sqlite:///password_detector.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Email Configuration
app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT', 587))
app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS', 'True').lower() == 'true'
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME', '')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD', '')
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER', 'noreply@passcheckerpro.com')
ADMIN_EMAIL = os.getenv('ADMIN_EMAIL', 'passcheckerpro@gmail.com')

# Initialize Mail
mail = Mail(app)

# Initialize extensions
from models import db, User, PasswordHistory, ContactMessage
db.init_app(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Prevent caching to ensure navbar always reflects current auth state
@app.after_request
def set_cache_headers(response):
    """Add cache-control headers to prevent caching and ensure navbar is always fresh"""
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate, private'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    return response

# Create tables
with app.app_context():
    db.create_all()

# Password generator utility
class PasswordAnalyzer:
    """Analyze password strength and check for common patterns"""
    
    # Common weak passwords and patterns
    COMMON_PASSWORDS = {
        'password', '123456', '123456789', 'qwerty', '12345678', '111111',
        'iloveyou', '123123', '1234567890', '000000', 'abc123', 'Password1',
        'password123', 'admin', 'letmein', 'welcome', 'monkey', 'dragon',
        'master', 'princess', 'qwertyuiop', 'solo', 'passw0rd'
    }
    
    @staticmethod
    def analyze_strength(password):
        """Analyze password strength and return detailed metrics"""
        score = 0
        feedback = []
        checks = {
            'length': False,
            'lowercase': False,
            'uppercase': False,
            'numbers': False,
            'special': False,
            'no_common': True,
            'no_repeat': True,
            'no_sequential': True
        }
        
        # Length check
        if len(password) >= 8:
            score += 20
            checks['length'] = True
            if len(password) >= 12:
                score += 10
            if len(password) >= 16:
                score += 10
        else:
            feedback.append("Password should be at least 8 characters long")
        
        # Lowercase letters
        if re.search(r'[a-z]', password):
            score += 15
            checks['lowercase'] = True
        else:
            feedback.append("Add lowercase letters")
        
        # Uppercase letters
        if re.search(r'[A-Z]', password):
            score += 15
            checks['uppercase'] = True
        else:
            feedback.append("Add uppercase letters")
        
        # Numbers
        if re.search(r'\d', password):
            score += 15
            checks['numbers'] = True
        else:
            feedback.append("Add numbers")
        
        # Special characters
        if re.search(r'[!@#$%^&*()_+\-=\[\]{};:\'",.<>?/]', password):
            score += 15
            checks['special'] = True
        else:
            feedback.append("Add special characters (!@#$%^&*)")
        
        # Check for common passwords
        if password.lower() in PasswordAnalyzer.COMMON_PASSWORDS:
            score = max(0, score - 40)
            checks['no_common'] = False
            feedback.append("This is a commonly used password")
        
        # Check for repeated characters
        if re.search(r'(.)\1{2,}', password):
            score = max(0, score - 20)
            checks['no_repeat'] = False
            feedback.append("Avoid repeating characters")
        
        # Check for sequential characters
        if re.search(r'(abc|bcd|cde|def|123|234|345|456)', password.lower()):
            score = max(0, score - 15)
            checks['no_sequential'] = False
            feedback.append("Avoid sequential characters")
        
        score = min(100, max(0, score))
        
        # Determine strength level
        if score >= 80:
            strength = 'Very Strong'
            color = '#27ae60'
        elif score >= 60:
            strength = 'Strong'
            color = '#2ecc71'
        elif score >= 40:
            strength = 'Medium'
            color = '#f39c12'
        elif score >= 20:
            strength = 'Weak'
            color = '#e74c3c'
        else:
            strength = 'Very Weak'
            color = '#c0392b'
        
        return {
            'score': score,
            'strength': strength,
            'color': color,
            'checks': checks,
            'feedback': feedback,
            'breached': False  # Simulation - in production, check against breach database
        }
    
    @staticmethod
    def check_breach_status(password):
        """Simulate breach detection - in production, check against Have I Been Pwned API"""
        return False  # Simulated - would check real breach database
    
    @staticmethod
    def generate_password(length=12, use_uppercase=True, use_numbers=True, use_special=True):
        """Generate a secure random password"""
        import random
        import string
        
        chars = string.ascii_lowercase
        if use_uppercase:
            chars += string.ascii_uppercase
        if use_numbers:
            chars += string.digits
        if use_special:
            chars += '!@#$%^&*()_+-=[]{}:;,.<>?'
        
        password = ''.join(random.choice(chars) for _ in range(length))
        return password

# Routes

@app.route('/')
@app.route('/welcome')
def welcome():
    """Welcome/Home page - redirect authenticated users to password tool"""
    if current_user.is_authenticated:
        return redirect(url_for('password_tool'))
    return render_template('welcome.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration"""
    if request.method == 'POST':
        data = request.get_json()
        
        # Validation
        if not data.get('username') or not data.get('email') or not data.get('password'):
            return jsonify({'success': False, 'error': 'All fields are required'}), 400
        
        if data['password'] != data['confirm_password']:
            return jsonify({'success': False, 'error': 'Passwords do not match'}), 400
        
        if len(data['password']) < 8:
            return jsonify({'success': False, 'error': 'Password must be at least 8 characters'}), 400
        
        # Check if user exists
        if User.query.filter_by(username=data['username']).first():
            return jsonify({'success': False, 'error': 'Username already exists'}), 400
        
        if User.query.filter_by(email=data['email']).first():
            return jsonify({'success': False, 'error': 'Email already registered'}), 400
        
        # Create new user
        user = User(
            username=data['username'],
            email=data['email'],
            mother_name=data['mother_name'],
            date_of_birth=data['date_of_birth'],
            favorite_color=data['favorite_color']
        )
        user.set_password(data['password'])
        
        try:
            db.session.add(user)
            db.session.commit()
            return jsonify({'success': True, 'message': 'Registration successful! Please login.'}), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({'success': False, 'error': str(e)}), 500
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    if request.method == 'POST':
        data = request.get_json()
        
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            return jsonify({'success': False, 'error': 'Username and password required'}), 400
        
        user = User.query.filter(
            (User.username == username) | (User.email == username)
        ).first()
        
        if user and user.check_password(password):
            login_user(user, remember=data.get('remember', False))
            return jsonify({'success': True, 'message': 'Login successful!'}), 200
        
        return jsonify({'success': False, 'error': 'Invalid username or password'}), 401
    
    return render_template('login.html')

@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    """Forgot password - initiate recovery"""
    if request.method == 'POST':
        data = request.get_json()
        identifier = data.get('identifier')
        
        user = User.query.filter(
            (User.username == identifier) | (User.email == identifier)
        ).first()
        
        if user:
            session['reset_user_id'] = user.id
            session['reset_step'] = 'security_questions'
            return jsonify({'success': True, 'message': 'Proceed to security verification'}), 200
        
        return jsonify({'success': False, 'error': 'User not found'}), 404
    
    return render_template('forgot_password.html')

@app.route('/security-verification', methods=['GET', 'POST'])
def security_verification():
    """Verify security questions"""
    if 'reset_user_id' not in session:
        return redirect(url_for('forgot_password'))
    
    user = User.query.get(session['reset_user_id'])
    
    if request.method == 'POST':
        data = request.get_json()
        
        # Verify answers (case-insensitive, whitespace-trimmed)
        mother_match = data.get('mother_name', '').strip().lower() == user.mother_name.lower()
        dob_match = data.get('date_of_birth', '').strip() == user.date_of_birth
        color_match = data.get('favorite_color', '').strip().lower() == user.favorite_color.lower()
        
        if mother_match and dob_match and color_match:
            session['reset_verified'] = True
            return jsonify({'success': True, 'message': 'Verification successful!'}), 200
        
        return jsonify({'success': False, 'error': 'Incorrect answers'}), 401
    
    return render_template('security_verification.html')

@app.route('/reset-password', methods=['GET', 'POST'])
def reset_password():
    """Reset password"""
    if 'reset_user_id' not in session or not session.get('reset_verified'):
        return redirect(url_for('forgot_password'))
    
    user = User.query.get(session['reset_user_id'])
    
    if request.method == 'POST':
        data = request.get_json()
        
        if not data.get('new_password'):
            return jsonify({'success': False, 'error': 'Password is required'}), 400
        
        if data['new_password'] != data.get('confirm_password'):
            return jsonify({'success': False, 'error': 'Passwords do not match'}), 400
        
        if len(data['new_password']) < 8:
            return jsonify({'success': False, 'error': 'Password must be at least 8 characters'}), 400
        
        user.set_password(data['new_password'])
        db.session.commit()
        
        # Clear session
        session.clear()
        
        return jsonify({'success': True, 'message': 'Password reset successful!'}), 200
    
    return render_template('reset_password.html')

@app.route('/dashboard')
@login_required
def dashboard():
    """User dashboard"""
    # Get statistics
    password_records = PasswordHistory.query.filter_by(user_id=current_user.id).all()
    
    total_checked = len(password_records)
    strong_count = len([p for p in password_records if p.strength in ['Strong', 'Very Strong']])
    weak_count = len([p for p in password_records if p.strength in ['Weak', 'Very Weak']])
    breached_count = len([p for p in password_records if p.breach_status])
    
    stats = {
        'total_checked': total_checked,
        'strong_passwords': strong_count,
        'weak_passwords': weak_count,
        'breached_passwords': breached_count
    }
    
    return render_template('dashboard.html', stats=stats, user=current_user)

@app.route('/password-tool')
@login_required
def password_tool():
    """Main password detection tool"""
    return render_template('password_tool.html')

@app.route('/api/analyze-password', methods=['POST'])
@login_required
def analyze_password():
    """API endpoint to analyze password strength"""
    data = request.get_json()
    password = data.get('password', '')
    
    if not password:
        return jsonify({'error': 'Password is required'}), 400
    
    analysis = PasswordAnalyzer.analyze_strength(password)
    breach_status = PasswordAnalyzer.check_breach_status(password)
    
    # Save to history
    record = PasswordHistory(
        user_id=current_user.id,
        password_checked=password,
        strength=analysis['strength'],
        breach_status=breach_status,
        score=analysis['score'],
        date_checked=datetime.now()
    )
    db.session.add(record)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'analysis': analysis,
        'breach_status': breach_status
    }), 200

@app.route('/api/generate-password', methods=['POST'])
@login_required
def generate_password():
    """API endpoint to generate secure password"""
    data = request.get_json()
    
    length = data.get('length', 12)
    use_uppercase = data.get('use_uppercase', True)
    use_numbers = data.get('use_numbers', True)
    use_special = data.get('use_special', True)
    
    password = PasswordAnalyzer.generate_password(
        length=length,
        use_uppercase=use_uppercase,
        use_numbers=use_numbers,
        use_special=use_special
    )
    
    return jsonify({
        'success': True,
        'password': password
    }), 200

@app.route('/api/password-history')
@login_required
def password_history():
    """Get user's password check history"""
    records = PasswordHistory.query.filter_by(user_id=current_user.id).order_by(
        PasswordHistory.date_checked.desc()
    ).all()
    
    history = [{
        'id': r.id,
        'password_checked': r.password_checked,
        'strength': r.strength,
        'score': r.score,
        'breach_status': r.breach_status,
        'date_checked': r.date_checked.strftime('%Y-%m-%d %H:%M:%S')
    } for r in records]
    
    return jsonify({'success': True, 'history': history}), 200

@app.route('/api/password-history/<int:record_id>', methods=['DELETE'])
@login_required
def delete_password_record(record_id):
    """Delete a specific password history record"""
    record = PasswordHistory.query.filter_by(id=record_id, user_id=current_user.id).first()
    
    if not record:
        return jsonify({'success': False, 'error': 'Record not found'}), 404
    
    db.session.delete(record)
    db.session.commit()
    
    return jsonify({'success': True, 'message': 'Record deleted'}), 200

@app.route('/api/password-history', methods=['DELETE'])
@login_required
def delete_all_history():
    """Delete all password history records for the user"""
    PasswordHistory.query.filter_by(user_id=current_user.id).delete()
    db.session.commit()
    
    return jsonify({'success': True, 'message': 'All history deleted'}), 200

@app.route('/api/statistics')
@login_required
def statistics():
    """Get dashboard statistics"""
    records = PasswordHistory.query.filter_by(user_id=current_user.id).all()
    
    strength_counts = {
        'Very Strong': 0,
        'Strong': 0,
        'Medium': 0,
        'Weak': 0,
        'Very Weak': 0
    }
    
    for record in records:
        if record.strength in strength_counts:
            strength_counts[record.strength] += 1
    
    return jsonify({
        'success': True,
        'statistics': strength_counts
    }), 200

@app.route('/api/contact', methods=['POST'])
def submit_contact():
    """Handle contact/feedback form submission with email notification"""
    try:
        data = request.get_json()
        name = data.get('name', '').strip()
        email = data.get('email', '').strip()
        message = data.get('message', '').strip()
        
        # Validation
        if not name or len(name) < 2:
            return jsonify({'success': False, 'error': 'Name must be at least 2 characters'}), 400
        
        if not email or not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            return jsonify({'success': False, 'error': 'Please provide a valid email address'}), 400
        
        if not message or len(message) < 5:
            return jsonify({'success': False, 'error': 'Message must be at least 5 characters'}), 400
        
        # Create and save contact message to database
        contact_msg = ContactMessage(name=name, email=email, message=message)
        db.session.add(contact_msg)
        db.session.commit()
        
        # Send email notification to admin
        try:
            if app.config['MAIL_USERNAME'] and app.config['MAIL_PASSWORD']:
                # Email to admin
                admin_msg = Message(
                    subject=f'New Contact Form Submission from {name}',
                    recipients=[ADMIN_EMAIL],
                    html=f"""
                    <div style="font-family: Arial, sans-serif; color: #333;">
                        <h2 style="color: #667eea;">New Contact Message</h2>
                        <p><strong>Name:</strong> {name}</p>
                        <p><strong>Email:</strong> <a href="mailto:{email}">{email}</a></p>
                        <p><strong>Message:</strong></p>
                        <div style="background: #f5f5f5; padding: 15px; border-radius: 5px; margin: 10px 0;">
                            {message.replace(chr(10), '<br>')}
                        </div>
                        <hr style="border: none; border-top: 1px solid #ddd; margin: 20px 0;">
                        <p style="font-size: 12px; color: #999;">
                            This is an automated message from PassChecker Pro Contact Form.
                        </p>
                    </div>
                    """
                )
                mail.send(admin_msg)
                
                # Send confirmation email to user
                user_msg = Message(
                    subject='We Received Your Message - PassChecker Pro',
                    recipients=[email],
                    html=f"""
                    <div style="font-family: Arial, sans-serif; color: #333;">
                        <h2 style="color: #667eea;">Thank You for Contacting Us!</h2>
                        <p>Hi {name},</p>
                        <p>We've received your message and we're grateful for reaching out. Our team will review your feedback and get back to you as soon as possible.</p>
                        <div style="background: #f5f5f5; padding: 15px; border-radius: 5px; margin: 20px 0;">
                            <p><strong>Your Message:</strong></p>
                            {message.replace(chr(10), '<br>')}
                        </div>
                        <p>In the meantime, feel free to continue using PassChecker Pro to secure your passwords.</p>
                        <p>Best regards,<br><strong>PassChecker Pro Team</strong></p>
                        <hr style="border: none; border-top: 1px solid #ddd; margin: 20px 0;">
                        <p style="font-size: 12px; color: #999;">
                            This is an automated confirmation email. Please do not reply to this email.
                        </p>
                    </div>
                    """
                )
                mail.send(user_msg)
        except Exception as e:
            # Email sending failed, but message is saved in database
            print(f"Email sending failed: {str(e)}")
            
        return jsonify({
            'success': True,
            'message': 'Thank you! Your message has been received. We\'ll get back to you soon.'
        }), 201
    
    except Exception as e:
        print(f"Contact form error: {str(e)}")
        return jsonify({'success': False, 'error': 'An error occurred. Please try again.'}), 500

@app.route('/admin/messages')
def view_contact_messages():
    """Admin page to view all contact messages"""
    # Get all messages sorted by latest first
    messages = ContactMessage.query.order_by(ContactMessage.submitted_at.desc()).all()
    return render_template('admin_messages.html', messages=messages, total=len(messages))

@app.route('/api/contact-message/<int:message_id>', methods=['DELETE'])
@login_required
def delete_contact_message(message_id):
    """Delete a specific contact message - Admin only"""
    try:
        message = ContactMessage.query.get(message_id)
        if not message:
            return jsonify({'success': False, 'error': 'Message not found'}), 404
        
        db.session.delete(message)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Message deleted successfully'}), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/logout')
def logout():
    """User logout - clear session and redirect to welcome page"""
    logout_user()
    session.clear()
    
    # Create response and redirect to welcome page
    response = redirect(url_for('welcome'))
    
    # Set headers to prevent caching of authenticated content
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate, private'
    response.headers['Pragma'] = 'no-cache, no-store, must-revalidate'
    response.headers['Expires'] = '0'
    response.headers['X-UA-Compatible'] = 'no-cache'
    
    return response

@app.route('/profile')
@login_required
def profile():
    """User profile page"""
    return render_template('profile.html', user=current_user)

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(error):
    """Handle 500 errors"""
    return render_template('500.html'), 500

if __name__ == '__main__':
    # Production configuration
    if os.getenv('FLASK_ENV') == 'production':
        app.run(host='0.0.0.0', port=int(os.getenv('PORT', 5000)))
    else:
        # Development configuration
        app.run(debug=True, host='0.0.0.0', port=5000)
