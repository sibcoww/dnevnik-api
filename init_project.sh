#!/bin/bash

# Initialize Django Project Script
# This script sets up the project with all necessary configurations

echo "🚀 Initializing Dnevnik API Project..."

# Check if .env exists
if [ ! -f .env ]; then
    echo "📋 Creating .env file from .env.example..."
    cp .env.example .env
    echo "✓ .env created. Please update it with your configuration."
else
    echo "✓ .env file already exists."
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "🔧 Creating virtual environment..."
    python -m venv venv
    echo "✓ Virtual environment created."
else
    echo "✓ Virtual environment already exists."
fi

# Activate virtual environment
echo "🔌 Activating virtual environment..."
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then
    # Windows
    source venv/Scripts/activate
else
    # Linux/Mac
    source venv/bin/activate
fi

# Install dependencies
echo "📦 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt
echo "✓ Dependencies installed."

# Create logs directory
mkdir -p logs

# Run migrations
echo "🗄️  Running database migrations..."
python manage.py migrate
echo "✓ Migrations completed."

# Create superuser
echo "👤 Creating superuser..."
python manage.py createsuperuser

# Collect static files
echo "📂 Collecting static files..."
python manage.py collectstatic --noinput
echo "✓ Static files collected."

# Create test data (optional)
read -p "Do you want to create test data? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "📊 Creating test data..."
    python manage.py shell < create_test_data.py
    echo "✓ Test data created."
fi

echo ""
echo "✅ Project initialization complete!"
echo ""
echo "📚 Next steps:"
echo "1. Run the development server: python manage.py runserver"
echo "2. Visit http://localhost:8000/admin/ to access admin panel"
echo "3. Visit http://localhost:8000/api/docs/ for API documentation"
echo ""
