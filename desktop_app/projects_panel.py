"""
Projects Panel for managing saved projects.
Provides list of saved projects and quick access.
"""
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
    QListWidget, QListWidgetItem, QMessageBox, QDialog,
    QDialogButtonBox, QFormLayout, QLineEdit, QTextEdit,
    QListWidget, QHeaderView, QTableWidget, QTableWidgetItem,
    QDateEdit, QVBoxLayout
)
from PyQt6.QtCore import Qt, QDate

from desktop_app.database import (
    get_all_projects, get_project, delete_project
)


class ProjectsPanel(QWidget):
    """Panel for displaying saved projects."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.main_window = parent
        self.init_ui()
        self.load_projects()
        
    def init_ui(self):
        """Initialize the user interface."""
        layout = QVBoxLayout(self)
        
        # Header
        header_layout = QHBoxLayout()
        
        title_label = QLabel("📁 Projects")
        font = title_label.font()
        font.setBold(True)
        title_label.setFont(font)
        header_layout.addWidget(title_label)
        
        # Refresh button
        self.refresh_btn = QPushButton("🔄")
        self.refresh_btn.setMaximumSize(30, 30)
        self.refresh_btn.clicked.connect(self.load_projects)
        header_layout.addWidget(self.refresh_btn)
        
        layout.addLayout(header_layout)
        
        # Projects list
        self.projects_list = QListWidget()
        self.projects_list.itemDoubleClicked.connect(self.load_project)
        self.projects_list.setMaximumHeight(250)
        layout.addWidget(self.projects_list)
        
        # Project details area
        self.details_widget = QWidget()
        self.details_widget.setVisible(False)
        details_layout = QVBoxLayout(self.details_widget)
        
        # Project info
        self.project_name_label = QLabel()
        font = self.project_name_label.font()
        font.setBold(True)
        font.setPointSize(12)
        self.project_name_label.setFont(font)
        self.project_name_label.setWordWrap(True)
        details_layout.addWidget(self.project_name_label)
        
        self.project_info_label = QLabel()
        self.project_info_label.setWordWrap(True)
        self.project_info_label.setStyleSheet("color: #666;")
        details_layout.addWidget(self.project_info_label)
        
        self.project_cost_label = QLabel()
        self.project_cost_label.setStyleSheet("color: #2e7d32; font-weight: bold;")
        details_layout.addWidget(self.project_cost_label)
        
        layout.addWidget(self.details_widget)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        # Load button
        self.load_btn = QPushButton("📂 Load")
        self.load_btn.clicked.connect(self.load_selected_project)
        self.load_btn.setEnabled(False)
        button_layout.addWidget(self.load_btn)
        
        # Delete button
        self.delete_btn = QPushButton("🗑️ Delete")
        self.delete_btn.clicked.connect(self.delete_selected_project)
        self.delete_btn.setEnabled(False)
        button_layout.addWidget(self.delete_btn)
        
        layout.addLayout(button_layout)
        
        # Connect signals
        self.projects_list.itemSelectionChanged.connect(self.on_selection_changed)
        
    def load_projects(self):
        """Load projects from database."""
        self.projects_list.clear()
        self.projects = get_all_projects()
        
        for project in self.projects:
            # Create list item with project info
            item = QListWidgetItem()
            item.setText(f"{project.name}")
            item.setToolTip(f"Created: {project.created_at.strftime('%Y-%m-%d %H:%M')}")
            item.setData(Qt.ItemDataRole.UserRole, project)
            
            # Set status based on creation date (recent = bold)
            font = item.font()
            if (project.created_at.date() == QDate.currentDate().toPython()):
                font.setBold(True)
            item.setFont(font)
            
            self.projects_list.addItem(item)
            
        # Clear selection
        self.projects_list.clearSelection()
        self.hide_project_details()
        
    def on_selection_changed(self):
        """Handle selection change."""
        selected_items = self.projects_list.selectedItems()
        has_selection = len(selected_items) > 0
        
        self.load_btn.setEnabled(has_selection)
        self.delete_btn.setEnabled(has_selection)
        
        if has_selection:
            self.show_project_details(selected_items[0])
        else:
            self.hide_project_details()
            
    def show_project_details(self, item):
        """Show details for the selected project."""
        project = item.data(Qt.ItemDataRole.UserRole)
        
        # Load full project with blocks
        try:
            full_project = get_project(project.id)
            
            self.project_name_label.setText(full_project.name)
            
            # Calculate project stats
            total_blocks = full_project.blocks.count()
            total_area = sum(
                (block.length / 12.0) * (block.width / 12.0) * float(block.block_type.price_per_sqft)
                for block in full_project.blocks.all()
            )
            
            self.project_info_label.setText(
                f"Created: {full_project.created_at.strftime('%Y-%m-%d %H:%M')}\n"
                f"Blocks: {total_blocks}"
            )
            
            self.project_cost_label.setText(f"Total Cost: ${total_area:,.2f}")
            
            self.details_widget.setVisible(True)
            
        except Exception as e:
            self.project_name_label.setText(full_project.name)
            self.project_info_label.setText(f"Error loading details: {str(e)}")
            self.project_cost_label.setText("")
            self.details_widget.setVisible(True)
            
    def hide_project_details(self):
        """Hide project details."""
        self.details_widget.setVisible(False)
        
    def get_selected_project(self):
        """Get the currently selected project."""
        current_item = self.projects_list.currentItem()
        if current_item:
            return current_item.data(Qt.ItemDataRole.UserRole)
        return None
        
    def load_selected_project(self):
        """Load the selected project."""
        project = self.get_selected_project()
        if project:
            self.load_project(project)
            
    def load_project(self, project):
        """Load a project into the calculator."""
        if hasattr(self.main_window, 'calculator_tab'):
            self.main_window.calculator_tab.load_project(project)
            
        # Switch to calculator tab
        if hasattr(self.main_window, 'tab_widget'):
            self.main_window.tab_widget.setCurrentIndex(0)
            
    def delete_selected_project(self):
        """Delete the selected project."""
        project = self.get_selected_project()
        if not project:
            return
            
        reply = QMessageBox.question(
            self, 'Delete Project', 
            f'Are you sure you want to delete project "{project.name}"?\n'
            f'This action cannot be undone.',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                delete_project(project.id)
                self.load_projects()
                QMessageBox.information(self, "Success", f"Project '{project.name}' deleted successfully!")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to delete project: {str(e)}")
                
    def refresh(self):
        """Refresh the projects list."""
        self.load_projects()