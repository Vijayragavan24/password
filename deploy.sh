#!/bin/bash
# Deployment Script for Password Detection Tool

echo "🚀 Starting deployment of Password Detection Tool..."

# Check if we're on PythonAnywhere
if [[ $HOSTNAME == *"pythonanywhere"* ]]; then
    echo "📍 Detected PythonAnywhere environment"

    # Install requirements
    echo "📦 Installing requirements..."
    pip install --user -r requirements.txt

    # Create database if it doesn't exist
    echo "🗄️ Setting up database..."
    python -c "
from app import app, db
with app.app_context():
    db.create_all()
    print('Database tables created successfully!')
"

    echo "✅ Deployment completed successfully!"
    echo "🌐 Your app should be available at: https://yourusername.pythonanywhere.com"

else
    echo "❌ This script is designed for PythonAnywhere deployment"
    echo "📖 Please follow the manual deployment guide in DEPLOYMENT.md"
fi