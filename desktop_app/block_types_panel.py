"""
Block Types Panel for managing block types.
Provides CRUD operations for block types.
"""
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
    QListWidget, QListWidgetItem, QMessageBox, QInputDialog,
    QDialog, QDialogButtonBox, QFormLayout, QLineEdit,
    QDoubleSpinBox, QListWidget, QHeaderView, QTableWidget,
    QTableWidgetItem
)
from PyQt6.QtCore import Qt

from desktop_app.database import (
    get_all_block_types, create_block_type, 
    update_block_type, delete_block_type
)


class BlockTypesPanel(QWidget):
    """Panel for managing block types."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.main_window = parent
        self.init_ui()
        self.load_block_types()
        
    def init_ui(self):
        """Initialize the user interface."""
        layout = QVBoxLayout(self)
        
        # Header
        header_layout = QHBoxLayout()
        
        title_label = QLabel("🏗️ Block Types")
        font = title_label.font()
        font.setBold(True)
        title_label.setFont(font)
        header_layout.addWidget(title_label)
        
        # Refresh button
        self.refresh_btn = QPushButton("🔄")
        self.refresh_btn.setMaximumSize(30, 30)
        self.refresh_btn.clicked.connect(self.load_block_types)
        header_layout.addWidget(self.refresh_btn)
        
        layout.addLayout(header_layout)
        
        # Block types table
        self.block_types_table = QTableWidget()
        self.block_types_table.setColumnCount(3)
        self.block_types_table.setHorizontalHeaderLabels(["Name", "Price/sqft", "Actions"])
        
        # Table settings
        header = self.block_types_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        
        self.block_types_table.verticalHeader().setVisible(False)
        self.block_types_table.setMaximumHeight(200)
        
        layout.addWidget(self.block_types_table)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        # Add button
        self.add_btn = QPushButton("➕ Add")
        self.add_btn.clicked.connect(self.add_block_type)
        button_layout.addWidget(self.add_btn)
        
        # Edit button
        self.edit_btn = QPushButton("✏️ Edit")
        self.edit_btn.clicked.connect(self.edit_block_type)
        self.edit_btn.setEnabled(False)
        button_layout.addWidget(self.edit_btn)
        
        # Delete button
        self.delete_btn = QPushButton("🗑️ Delete")
        self.delete_btn.clicked.connect(self.delete_block_type)
        self.delete_btn.setEnabled(False)
        button_layout.addWidget(self.delete_btn)
        
        layout.addLayout(button_layout)
        
        # Connect signals
        self.block_types_table.itemSelectionChanged.connect(self.on_selection_changed)
        self.block_types_table.doubleClicked.connect(self.edit_block_type)
        
    def load_block_types(self):
        """Load block types from database."""
        self.block_types = get_all_block_types()
        self.block_types_table.setRowCount(len(self.block_types))
        
        for row, block_type in enumerate(self.block_types):
            # Name
            name_item = QTableWidgetItem(block_type.name)
            name_item.setData(Qt.ItemDataRole.UserRole, block_type)
            self.block_types_table.setItem(row, 0, name_item)
            
            # Price per sqft
            price_item = QTableWidgetItem(f"${block_type.price_per_sqft}")
            self.block_types_table.setItem(row, 1, price_item)
            
            # Actions (placeholder for now)
            actions_item = QTableWidgetItem("🔧")
            actions_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.block_types_table.setItem(row, 2, actions_item)
            
        # Clear selection
        self.block_types_table.clearSelection()
        
    def on_selection_changed(self):
        """Handle selection change."""
        selected_items = self.block_types_table.selectedItems()
        has_selection = len(selected_items) > 0
        
        self.edit_btn.setEnabled(has_selection)
        self.delete_btn.setEnabled(has_selection)
        
    def get_selected_block_type(self):
        """Get the currently selected block type."""
        current_item = self.block_types_table.currentItem()
        if current_item and current_item.column() == 0:
            return current_item.data(Qt.ItemDataRole.UserRole)
        return None
        
    def add_block_type(self):
        """Add a new block type."""
        dialog = BlockTypeDialog(self)
        if dialog.exec():
            try:
                name, price = dialog.get_block_type_data()
                block_type = create_block_type(name, price)
                self.load_block_types()
                QMessageBox.information(self, "Success", f"Block type '{block_type.name}' created successfully!")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to create block type: {str(e)}")
                
    def edit_block_type(self):
        """Edit the selected block type."""
        block_type = self.get_selected_block_type()
        if not block_type:
            return
            
        dialog = BlockTypeDialog(self, block_type)
        if dialog.exec():
            try:
                name, price = dialog.get_block_type_data()
                update_block_type(block_type.id, name, price)
                self.load_block_types()
                QMessageBox.information(self, "Success", f"Block type '{name}' updated successfully!")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to update block type: {str(e)}")
                
    def delete_block_type(self):
        """Delete the selected block type."""
        block_type = self.get_selected_block_type()
        if not block_type:
            return
            
        reply = QMessageBox.question(
            self, 'Delete Block Type', 
            f'Are you sure you want to delete "{block_type.name}"?',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                delete_block_type(block_type.id)
                self.load_block_types()
                QMessageBox.information(self, "Success", f"Block type '{block_type.name}' deleted successfully!")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to delete block type: {str(e)}")
                
    def show_dialog(self):
        """Show the block types dialog (for menu access)."""
        self.setVisible(True)
        self.load_block_types()
        self.raise_()
        self.activateWindow()


class BlockTypeDialog(QDialog):
    """Dialog for adding/editing block types."""
    
    def __init__(self, parent=None, block_type=None):
        super().__init__(parent)
        self.block_type = block_type
        self.setWindowTitle("Add Block Type" if not block_type else "Edit Block Type")
        self.init_ui()
        
    def init_ui(self):
        """Initialize the dialog UI."""
        layout = QFormLayout(self)
        
        # Name
        self.name_input = QLineEdit()
        layout.addRow("Name:", self.name_input)
        
        # Price per sqft
        self.price_input = QDoubleSpinBox()
        self.price_input.setRange(0.01, 9999.99)
        self.price_input.setDecimals(2)
        self.price_input.setPrefix("$")
        layout.addRow("Price per sqft:", self.price_input)
        
        # Buttons
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addRow("", buttons)
        
        # Load existing data if editing
        if self.block_type:
            self.name_input.setText(self.block_type.name)
            self.price_input.setValue(float(self.block_type.price_per_sqft))
        else:
            self.price_input.setValue(50.00)  # Default price
            
    def get_block_type_data(self):
        """Get the block type data from the form."""
        name = self.name_input.text().strip()
        price = self.price_input.value()
        
        if not name:
            raise ValueError("Name is required")
        if price <= 0:
            raise ValueError("Price must be greater than 0")
            
        return name, price