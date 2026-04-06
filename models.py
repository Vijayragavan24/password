from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
import bcrypt

db = SQLAlchemy()

class User(UserMixin, db.Model):
    """User model for authentication"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    mother_name = db.Column(db.String(120), nullable=False)
    date_of_birth = db.Column(db.String(20), nullable=False)
    favorite_color = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    
    # Relationships
    password_history = db.relationship('PasswordHistory', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def set_password(self, password):
        """Hash and set password"""
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    def check_password(self, password):
        """Verify password"""
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))
    
    def __repr__(self):
        return f'<User {self.username}>'

class PasswordHistory(db.Model):
    """Password check history model"""
    __tablename__ = 'password_history'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    password_checked = db.Column(db.String(255), nullable=False)
    strength = db.Column(db.String(20), nullable=False)
    score = db.Column(db.Integer, default=0)
    breach_status = db.Column(db.Boolean, default=False)
    date_checked = db.Column(db.DateTime, default=datetime.now)
    
    def __repr__(self):
        return f'<PasswordHistory {self.id}>'

class ContactMessage(db.Model):
    """Contact/Feedback message model"""
    __tablename__ = 'contact_messages'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    message = db.Column(db.Text, nullable=False)
    submitted_at = db.Column(db.DateTime, default=datetime.now)
    
    def __repr__(self):
        return f'<ContactMessage {self.id}>'
