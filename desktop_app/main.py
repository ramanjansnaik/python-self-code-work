"""
Main entry point for the PyQt6 Desktop Application.
Replaces the Django web frontend with a native desktop GUI.
"""
import sys
import os

# Add the project directory to Python path for Django models
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set Django settings module before importing Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'precostcalc.settings')

import django
django.setup()

from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt6.QtCore import Qt
from desktop_app.main_window import MainWindow
from desktop_app.database import init_database


def main():
    """Main application entry point."""
    # Initialize database
    init_database()
    
    # Create and run the application
    app = QApplication(sys.argv)
    app.setApplicationName("PreCostCalc Desktop")
    app.setOrganizationName("PreCostCalc")
    
    # Apply a modern style
    app.setStyle("Fusion")
    
    # Create and show main window
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
