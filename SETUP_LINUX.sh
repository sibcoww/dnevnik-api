#!/bin/bash
# Setup Instructions for Linux/Mac Users

echo "╔════════════════════════════════════════════════════════╗"
echo "║  Dnevnik API - Setup Instructions (Linux/Mac)         ║"
echo "╚════════════════════════════════════════════════════════╝"
echo ""

echo "📋 Prerequisites:"
echo "  • Python 3.11+"
echo "  • PostgreSQL 12+"
echo "  • pip (Python package manager)"
echo ""

echo "🚀 Quick Setup (5 minutes):"
echo ""
echo "1️⃣  Create virtual environment:"
echo "   python3 -m venv venv"
echo "   source venv/bin/activate"
echo ""

echo "2️⃣  Install dependencies:"
echo "   pip install -r requirements.txt"
echo ""

echo "3️⃣  Create .env file:"
echo "   cp .env.example .env"
echo "   # Edit .env with your settings"
echo ""

echo "4️⃣  Create PostgreSQL database:"
echo "   createdb dnevnik_db"
echo ""

echo "5️⃣  Run migrations:"
echo "   python manage.py migrate"
echo ""

echo "6️⃣  Create superuser (admin):"
echo "   python manage.py createsuperuser"
echo ""

echo "7️⃣  Run development server:"
echo "   python manage.py runserver"
echo ""

echo "8️⃣  Open in browser:"
echo "   http://localhost:8000/api/docs/"
echo ""

echo "📚 Documentation:"
echo "  • 00_START_HERE.md      - Overview"
echo "  • README.md             - Full documentation"
echo "  • QUICKSTART.md         - Quick setup guide"
echo "  • API_EXAMPLES.md       - API examples"
echo "  • PROJECT_STRUCTURE.md  - Architecture"
echo "  • PRODUCTION.md         - Production deployment"
echo ""

echo "✨ Create test data (optional):"
echo "   python manage.py shell < create_test_data.py"
echo ""

echo "📞 Support:"
echo "  • Check documentation files above"
echo "  • Django admin: http://localhost:8000/admin/"
echo "  • API docs: http://localhost:8000/api/docs/"
echo ""

echo "✅ Ready to develop!"
