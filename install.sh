#!/bin/bash

echo "====================================="
echo "TestGen Installation Script"
echo "====================================="
echo ""

# Check Python version
echo "Checking Python version..."
python3 --version
if [ $? -ne 0 ]; then
    echo "Error: Python 3 is not installed"
    exit 1
fi

# Check Node.js version
echo "Checking Node.js version..."
node --version
if [ $? -ne 0 ]; then
    echo "Warning: Node.js is not installed. Frontend will not be available."
    echo "Install Node.js 18+ to use the React frontend."
    SKIP_FRONTEND=1
fi

echo ""
echo "Setting up backend..."
echo "====================="

# Create virtual environment
echo "Creating Python virtual environment..."
python3 -m venv .venv

# Activate virtual environment
source .venv/bin/activate

# Install Python dependencies
echo "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Run migrations
echo "Running database migrations..."
python manage.py migrate

# Create superuser
echo ""
echo "Create a superuser for Django admin:"
python manage.py createsuperuser

echo ""
echo "Backend setup complete!"

if [ -z "$SKIP_FRONTEND" ]; then
    echo ""
    echo "Setting up frontend..."
    echo "====================="
    
    cd frontend
    
    # Install Node dependencies
    echo "Installing Node.js dependencies..."
    npm install
    
    cd ..
    
    echo ""
    echo "Frontend setup complete!"
fi

echo ""
echo "====================================="
echo "Installation Complete!"
echo "====================================="
echo ""
echo "To start the application:"
echo ""
echo "Backend (Django):"
echo "  source .venv/bin/activate"
echo "  python manage.py runserver"
echo ""

if [ -z "$SKIP_FRONTEND" ]; then
    echo "Frontend (React):"
    echo "  cd frontend"
    echo "  npm start"
    echo ""
fi

echo "Access the application:"
if [ -z "$SKIP_FRONTEND" ]; then
    echo "  Frontend: http://localhost:3000"
fi
echo "  Backend API: http://localhost:8000"
echo "  Django Admin: http://localhost:8000/admin"
echo ""
echo "For more information, see README.md"
