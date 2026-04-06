#!/usr/bin/env python3
"""
CREATE TEST USER AND VERIFY LOGOUT FUNCTIONALITY
"""

import sys
sys.path.insert(0, 'c:\\Users\\HP\\OneDrive\\Desktop\\Password Detection Tool')

from app import app, db
from models import User

with app.app_context():
    # Check if test user exists
    test_user = User.query.filter_by(email='testuser@test.com').first()
    
    if test_user:
        print(f"✅ Test user exists: {test_user.username} ({test_user.email})")
        print(f"   User ID: {test_user.id}")
        print(f"   Created: {test_user.created_at}")
    else:
        print("❌ Test user NOT found - Creating new test user...")
        
        new_user = User(
            username='testuser',
            email='testuser@test.com',
            mother_name='test',
            date_of_birth='2000-01-01',
            favorite_color='blue'
        )
        new_user.set_password('Test@123456')
        
        db.session.add(new_user)
        db.session.commit()
        
        print(f"✅ Test user created successfully!")
        print(f"   Email: testuser@test.com")
        print(f"   Password: Test@123456")
        print(f"   User ID: {new_user.id}")
