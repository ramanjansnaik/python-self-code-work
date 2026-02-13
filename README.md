# PreCostCalc Desktop - Test Generator

A desktop application built with PyQt6 that replaces the Django + React web frontend with a native desktop GUI. Features dual functionality: cost estimation calculator and AI-powered test generation.

## 🏗️ Features

### Cost Calculator
- **Interactive Canvas**: Drag-and-drop block placement with real-time visual feedback
- **Cost Estimation**: Automatic cost calculation based on area and price per sqft
- **Project Management**: Save, load, and manage multiple projects
- **Block Types**: Customizable block types with pricing
- **Real-time Updates**: Instant cost and area calculations

### Test Generator
- **AI-Powered**: Generate automated tests using multiple LLM providers (OpenAI, Anthropic, Google, Ollama)
- **Multiple Frameworks**: Support for Playwright and Selenium
- **Multiple Languages**: Python, JavaScript, TypeScript, Java, C#
- **Project Organization**: Manage test projects and generated tests
- **Code Export**: Copy generated tests to clipboard or save to files

## 🚀 Quick Start

### Prerequisites
- Python 3.12+
- Django 5.2.4
- PyQt6 6.6.1+

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/ramanjansnaik/test-generator.git
   cd test-generator
   ```

2. **Install dependencies**:
   ```bash
   pip install -r pyqt6_requirements.txt
   ```

3. **Run the application**:
   ```bash
   python desktop_app/main.py
   ```

## 📦 Building from Source

### Windows (creates .exe)
```bash
# Using the build script
build_desktop.bat
```

### Linux/macOS
```bash
# Using the build script
chmod +x build_desktop.sh
./build_desktop.sh
```

### Manual Build
```bash
# Install dependencies
pip install -r pyqt6_requirements.txt

# Build with PyInstaller
pyinstaller precostcalc_desktop.spec --clean --noconfirm
```

The executable will be created in `dist/PreCostCalcDesktop` (Linux/macOS) or `dist/PreCostCalcDesktop.exe` (Windows).

## 🏛️ Architecture

### Desktop Application Structure
```
desktop_app/
├── main.py                 # Application entry point
├── main_window.py          # Main application window with tabs
├── database.py            # Django ORM integration
├── calculator_tab.py      # Cost calculator functionality
├── testgen_tab.py         # Test generator functionality
├── block_types_panel.py   # Block type management
└── projects_panel.py      # Project management panel
```

### Key Components

1. **MainWindow**: Primary interface with tabbed layout
   - Cost Calculator tab
   - Test Generator tab
   - Side panels for quick access

2. **Database Layer**: Direct Django ORM access
   - No REST API overhead
   - Direct model manipulation
   - SQLite database

3. **Calculator Tab**:
   - Interactive canvas for block placement
   - Real-time cost calculation
   - Project save/load functionality

4. **TestGen Tab**:
   - LLM provider configuration
   - Test project management
   - AI-powered test generation

## 🗄️ Database Schema

### Core Models (from Django)
- **BlockType**: Predefined block types with pricing
- **Project**: User projects containing blocks
- **BlockInstance**: Individual block placements
- **LLMProvider**: AI provider configurations
- **TestProject**: Test generation projects
- **GeneratedTest**: Saved generated tests

### Direct ORM Access
The desktop app uses Django ORM directly, bypassing the REST API:
```python
from desktop_app.database import get_all_block_types, create_project

# Get block types
block_types = get_all_block_types()

# Create a new project
project = create_project("My Project", blocks_data)
```

## 🔧 Configuration

### Default Block Types
- Standard Room: $50.00/sqft
- Premium Room: $75.00/sqft
- Bathroom: $100.00/sqft
- Kitchen: $120.00/sqft
- Garage: $35.00/sqft

### Database Location
SQLite database: `db.sqlite3`

### Application Settings
Modify `precostcalc/settings.py` for production deployment.

## 📋 Usage

### Cost Calculator
1. Select block types from the left panel
2. Click "Add Selected Block" to place on canvas
3. Drag blocks to position them
4. Adjust block dimensions in properties panel
5. View real-time cost calculations
6. Save projects for later use

### Test Generator
1. Configure LLM providers in the left panel
2. Create a test project with website URL
3. Select framework (Playwright/Selenium) and language
4. Click "Generate Tests" to create tests
5. Save generated tests or copy to clipboard

## 🛠️ Development

### Project Structure
```
.
├── desktop_app/              # PyQt6 desktop application
├── precostcalc/             # Django settings (for database)
├── calculator/              # Original Django models
├── testgen/                 # Test generation models
├── build_desktop.sh         # Linux/macOS build script
├── build_desktop.bat        # Windows build script
├── precostcalc_desktop.spec # PyInstaller configuration
└── pyqt6_requirements.txt   # Python dependencies
```

### Adding Features
1. **New Tab**: Create widget in `main_window.py`
2. **Database Operations**: Add functions to `database.py`
3. **UI Components**: Create panels in appropriate files

### Testing
```bash
# Test the application
python desktop_app/main.py

# Run database tests
python manage.py test calculator
```

## 🚚 Deployment

### Packaging
The application is packaged as a single executable using PyInstaller:
- No Python installation required for end users
- All dependencies included
- SQLite database bundled

### Distribution
- **Windows**: `dist/PreCostCalcDesktop.exe`
- **Linux**: `dist/PreCostCalcDesktop`
- **macOS**: `dist/PreCostCalcDesktop`

### File Size
- Approximately 70MB including all dependencies
- Compressed database storage
- No external Python runtime needed

## 🔄 Migration from Web Version

The desktop app replaces:
- ❌ Django web server
- ❌ React frontend
- ❌ REST API endpoints
- ❌ Web authentication

With:
- ✅ PyQt6 desktop interface
- ✅ Direct Django ORM access
- ✅ Native file system operations
- ✅ Local data storage

## 📊 Performance

### Advantages
- **No Network Overhead**: Direct database access
- **Fast Startup**: No web server initialization
- **Native UI**: Better performance and user experience
- **Offline Operation**: No internet connection required

### Benchmarks
- Application startup: < 5 seconds
- Canvas rendering: 60 FPS
- Cost calculation: Real-time
- Database operations: < 100ms

## 🔒 Security

### Local Data Storage
- SQLite database stored locally
- No network transmission of data
- User authentication via Django admin

### API Keys
- Stored locally in database
- Encrypted at rest
- No cloud storage

## 📄 License

See LICENSE file for details.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📞 Support

For issues and questions:
- GitHub Issues: [Repository Issues](https://github.com/ramanjansnaik/test-generator/issues)
- Documentation: This README
- Architecture: See code comments

## 🎯 Roadmap

### Upcoming Features
- [ ] Dark mode theme
- [ ] Export projects to PDF
- [ ] Cloud synchronization
- [ ] Additional test frameworks
- [ ] Batch test generation
- [ ] Project templates

### Completed Features
- [x] PyQt6 desktop interface
- [x] Interactive cost calculator
- [x] AI-powered test generation
- [x] Project management
- [x] Single-executable packaging
- [x] Direct ORM integration

---

**Built with ❤️ using PyQt6 and Django ORM**