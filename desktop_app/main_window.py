"""
Main window for the PyQt6 Desktop Application.
Provides a tabbed interface for both Calculator and TestGen functionality.
"""
import sys
from PyQt6.QtWidgets import (
    QMainWindow, QTabWidget, QVBoxLayout, QHBoxLayout, QWidget, 
    QMenuBar, QMenu, QToolBar, QStatusBar, QLabel, QMessageBox,
    QDockWidget, QListWidget, QSplitter
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QAction, QIcon

from desktop_app.calculator_tab import CalculatorTab
from desktop_app.testgen_tab import TestGenTab
from desktop_app.block_types_panel import BlockTypesPanel
from desktop_app.projects_panel import ProjectsPanel


class MainWindow(QMainWindow):
    """Main application window with tabbed interface."""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.setup_menu_bar()
        self.setup_tool_bar()
        self.setup_status_bar()
        self.setup_docks()
        
    def init_ui(self):
        """Initialize the user interface."""
        self.setWindowTitle("PreCostCalc Desktop - Test Generator")
        self.setMinimumSize(1200, 800)
        
        # Central widget with tabs
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        # Main layout
        main_layout = QHBoxLayout(self.central_widget)
        
        # Create main splitter
        self.main_splitter = QSplitter(Qt.Orientation.Horizontal)
        main_layout.addWidget(self.main_splitter)
        
        # Left dock area for panels
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        self.main_splitter.addWidget(left_widget)
        
        # Tab widget for main content
        self.tab_widget = QTabWidget()
        self.main_splitter.addWidget(self.tab_widget)
        
        # Initialize tabs
        self.calculator_tab = CalculatorTab(self)
        self.testgen_tab = TestGenTab(self)
        
        self.tab_widget.addTab(self.calculator_tab, "🏗️ Cost Calculator")
        self.tab_widget.addTab(self.testgen_tab, "🧪 Test Generator")
        
        # Set splitter proportions
        self.main_splitter.setStretchFactor(0, 1)
        self.main_splitter.setStretchFactor(1, 3)
        
        # Block types panel
        self.block_types_panel = BlockTypesPanel(self)
        
        # Projects panel  
        self.projects_panel = ProjectsPanel(self)
        
        # Add panels to left layout
        left_layout.addWidget(self.block_types_panel)
        left_layout.addWidget(self.projects_panel)
        left_layout.addStretch()
        
    def setup_menu_bar(self):
        """Create the menu bar."""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu('File')
        
        # New project action
        new_project_action = QAction('New Project', self)
        new_project_action.setShortcut('Ctrl+N')
        new_project_action.triggered.connect(self.new_project)
        file_menu.addAction(new_project_action)
        
        # Open project action
        open_project_action = QAction('Open Project', self)
        open_project_action.setShortcut('Ctrl+O')
        open_project_action.triggered.connect(self.open_project)
        file_menu.addAction(open_project_action)
        
        # Save project action
        save_project_action = QAction('Save Project', self)
        save_project_action.setShortcut('Ctrl+S')
        save_project_action.triggered.connect(self.save_project)
        file_menu.addAction(save_project_action)
        
        file_menu.addSeparator()
        
        # Exit action
        exit_action = QAction('Exit', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Edit menu
        edit_menu = menubar.addMenu('Edit')
        
        # Block types action
        block_types_action = QAction('Block Types...', self)
        block_types_action.triggered.connect(self.manage_block_types)
        edit_menu.addAction(block_types_action)
        
        # Settings action
        settings_action = QAction('Settings...', self)
        settings_action.triggered.connect(self.open_settings)
        edit_menu.addAction(settings_action)
        
        # Tools menu
        tools_menu = menubar.addMenu('Tools')
        
        # Test generator action
        testgen_action = QAction('Test Generator', self)
        testgen_action.triggered.connect(lambda: self.tab_widget.setCurrentIndex(1))
        tools_menu.addAction(testgen_action)
        
        # Calculator action
        calculator_action = QAction('Cost Calculator', self)
        calculator_action.triggered.connect(lambda: self.tab_widget.setCurrentIndex(0))
        tools_menu.addAction(calculator_action)
        
        # Help menu
        help_menu = menubar.addMenu('Help')
        
        # About action
        about_action = QAction('About', self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
        
    def setup_tool_bar(self):
        """Create the toolbar."""
        toolbar = self.addToolBar('Main')
        toolbar.setMovable(False)
        
        # New project button
        new_project_action = QAction('New Project', self)
        new_project_action.triggered.connect(self.new_project)
        toolbar.addAction(new_project_action)
        
        # Save project button
        save_project_action = QAction('Save', self)
        save_project_action.triggered.connect(self.save_project)
        toolbar.addAction(save_project_action)
        
        toolbar.addSeparator()
        
        # Calculator tab
        calc_action = QAction('Calculator', self)
        calc_action.triggered.connect(lambda: self.tab_widget.setCurrentIndex(0))
        toolbar.addAction(calc_action)
        
        # TestGen tab
        testgen_action = QAction('Test Generator', self)
        testgen_action.triggered.connect(lambda: self.tab_widget.setCurrentIndex(1))
        toolbar.addAction(testgen_action)
        
    def setup_status_bar(self):
        """Create the status bar."""
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        
        # Status label
        self.status_label = QLabel("Ready")
        self.status_bar.addWidget(self.status_label)
        
        # Progress indicator (hidden by default)
        self.progress_label = QLabel("")
        self.progress_label.hide()
        self.status_bar.addPermanentWidget(self.progress_label)
        
    def setup_docks(self):
        """Setup dockable panels."""
        # These are already integrated into the main layout
        # but could be made dockable in the future
        
        pass
        
    def new_project(self):
        """Create a new project."""
        current_tab = self.tab_widget.currentWidget()
        if hasattr(current_tab, 'new_project'):
            current_tab.new_project()
            
    def open_project(self):
        """Open an existing project."""
        current_tab = self.tab_widget.currentWidget()
        if hasattr(current_tab, 'open_project'):
            current_tab.open_project()
            
    def save_project(self):
        """Save the current project."""
        current_tab = self.tab_widget.currentWidget()
        if hasattr(current_tab, 'save_project'):
            current_tab.save_project()
            
    def manage_block_types(self):
        """Open block types management dialog."""
        self.block_types_panel.show_dialog()
        
    def open_settings(self):
        """Open application settings."""
        QMessageBox.information(self, "Settings", "Settings dialog not implemented yet.")
        
    def show_about(self):
        """Show about dialog."""
        QMessageBox.about(
            self, 
            "About PreCostCalc Desktop",
            "PreCostCalc Desktop v1.0.0\n\n"
            "A desktop application for cost estimation and automated test generation.\n\n"
            "Built with PyQt6 and Django ORM integration."
        )
        
    def update_status(self, message):
        """Update the status bar message."""
        self.status_label.setText(message)
        
    def show_progress(self, message):
        """Show progress indicator in status bar."""
        self.progress_label.setText(message)
        self.progress_label.show()
        
    def hide_progress(self):
        """Hide progress indicator."""
        self.progress_label.hide()
        
    def closeEvent(self, event):
        """Handle application close event."""
        reply = QMessageBox.question(
            self, 
            'Confirm Exit',
            'Are you sure you want to exit?',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            event.accept()
        else:
            event.ignore()