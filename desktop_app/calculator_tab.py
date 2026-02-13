"""
Calculator tab for the PyQt6 Desktop Application.
Provides interactive block placement and cost calculation.
"""
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
    QSpinBox, QDoubleSpinBox, QListWidget, QListWidgetItem,
    QGroupBox, QSplitter, QMessageBox, QInputDialog, QColorDialog,
    QFrame, QScrollArea
)
from PyQt6.QtCore import Qt, QRectF, QPointF, pyqtSignal, QTimer
from PyQt6.QtGui import QPainter, QColor, QPen, QBrush, QFont, QPainterPath

from desktop_app.database import (
    get_all_block_types, create_block_type, update_block_type, delete_block_type,
    get_all_projects, get_project, create_project, update_project, delete_project
)


class BlockItem:
    """Represents a block instance on the canvas."""
    
    def __init__(self, block_type_id, name, price_per_sqft, length=100, width=100, x=0, y=0, color=None):
        self.block_type_id = block_type_id
        self.name = name
        self.price_per_sqft = price_per_sqft
        self.length = length
        self.width = width
        self.x = x
        self.y = y
        self.color = color or QColor(100, 150, 200)
        
    def to_dict(self):
        """Convert to dictionary for saving."""
        return {
            'block_type_id': self.block_type_id,
            'length': self.length,
            'width': self.width,
            'x': self.x,
            'y': self.y
        }
        
    @property
    def area(self):
        """Calculate area in square feet."""
        return (self.length / 12.0) * (self.width / 12.0)  # Convert inches to feet
        
    @property
    def cost(self):
        """Calculate cost based on area and price per sqft."""
        return self.area * float(self.price_per_sqft)
        
    def contains_point(self, px, py):
        """Check if a point is within this block."""
        return (self.x <= px <= self.x + self.length and 
                self.y <= py <= self.y + self.width)


class CanvasWidget(QWidget):
    """Interactive canvas for drawing and placing blocks."""
    
    block_clicked = pyqtSignal(object)
    block_moved = pyqtSignal(object, int, int)
    canvas_clicked = pyqtSignal(int, int)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.blocks = []
        self.selected_block = None
        self.is_dragging = False
        self.drag_offset_x = 0
        self.drag_offset_y = 0
        self.setMinimumSize(800, 600)
        self.setStyleSheet("background-color: #f5f5f5; border: 1px solid #ccc;")
        
    def add_block(self, block):
        """Add a block to the canvas."""
        self.blocks.append(block)
        self.update()
        
    def remove_block(self, block):
        """Remove a block from the canvas."""
        if block in self.blocks:
            self.blocks.remove(block)
            if self.selected_block == block:
                self.selected_block = None
            self.update()
        
    def clear_canvas(self):
        """Clear all blocks from canvas."""
        self.blocks = []
        self.selected_block = None
        self.update()
        
    def select_block_at(self, x, y):
        """Select a block at the given position."""
        # Check from top to bottom (reverse order for z-order)
        for block in reversed(self.blocks):
            if block.contains_point(x, y):
                self.selected_block = block
                return block
        self.selected_block = None
        return None
        
    def mousePressEvent(self, event):
        """Handle mouse press event."""
        x = event.position().x()
        y = event.position().y()
        
        block = self.select_block_at(x, y)
        if block:
            self.selected_block = block
            self.is_dragging = True
            self.drag_offset_x = x - block.x
            self.drag_offset_y = y - block.y
            self.block_clicked.emit(block)
        else:
            self.selected_block = None
            self.canvas_clicked.emit(x, y)
        self.update()
        
    def mouseMoveEvent(self, event):
        """Handle mouse move event."""
        if self.is_dragging and self.selected_block:
            x = event.position().x()
            y = event.position().y()
            self.selected_block.x = x - self.drag_offset_x
            self.selected_block.y = y - self.drag_offset_y
            self.block_moved.emit(self.selected_block, int(self.selected_block.x), int(self.selected_block.y))
            self.update()
            
    def mouseReleaseEvent(self, event):
        """Handle mouse release event."""
        self.is_dragging = False
        
    def paintEvent(self, event):
        """Paint the canvas and blocks."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Draw grid
        self.draw_grid(painter)
        
        # Draw blocks
        for block in self.blocks:
            self.draw_block(painter, block, block == self.selected_block)
            
    def draw_grid(self, painter):
        """Draw a grid on the canvas."""
        painter.setPen(QPen(QColor(220, 220, 220), 1))
        
        # Draw vertical lines (every 50 pixels = ~5 feet at scale)
        for x in range(0, self.width(), 50):
            painter.drawLine(x, 0, x, self.height())
            
        # Draw horizontal lines
        for y in range(0, self.height(), 50):
            painter.drawLine(0, y, self.width(), y)
            
    def draw_block(self, painter, block, selected):
        """Draw a single block on the canvas."""
        # Draw block rectangle
        rect = QRectF(block.x, block.y, block.length, block.width)
        
        # Fill
        brush = QBrush(block.color)
        if selected:
            brush.setColor(block.color.darker(120))
        painter.setBrush(brush)
        
        # Border
        pen = QPen(QColor(50, 50, 50), 2 if selected else 1)
        painter.setPen(pen)
        painter.drawRect(rect)
        
        # Draw label
        painter.setPen(Qt.GlobalColor.black)
        font = QFont()
        font.setPointSize(10)
        painter.setFont(font)
        
        # Calculate cost
        cost_text = f"${block.cost:.2f}"
        area_text = f"{block.area:.1f} sqft"
        
        # Draw text centered in block
        painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, f"{block.name}\n{cost_text}")
        
    def get_total_cost(self):
        """Calculate total cost of all blocks."""
        return sum(block.cost for block in self.blocks)
        
    def get_total_area(self):
        """Calculate total area of all blocks."""
        return sum(block.area for block in self.blocks)


class CalculatorTab(QWidget):
    """Tab widget for cost calculator functionality."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.main_window = parent
        self.current_project_id = None
        self.current_project_name = None
        self.blocks = []  # List of BlockItem objects
        self.init_ui()
        self.load_block_types()
        
    def init_ui(self):
        """Initialize the user interface."""
        layout = QVBoxLayout(self)
        
        # Top toolbar
        toolbar_layout = QHBoxLayout()
        
        # New project button
        self.new_btn = QPushButton("🆕 New Project")
        self.new_btn.clicked.connect(self.new_project)
        toolbar_layout.addWidget(self.new_btn)
        
        # Save button
        self.save_btn = QPushButton("💾 Save Project")
        self.save_btn.clicked.connect(self.save_project)
        toolbar_layout.addWidget(self.save_btn)
        
        # Clear canvas button
        self.clear_btn = QPushButton("🗑️ Clear Canvas")
        self.clear_btn.clicked.connect(self.clear_canvas)
        toolbar_layout.addWidget(self.clear_btn)
        
        toolbar_layout.addStretch()
        
        # Project name label
        self.project_name_label = QLabel("Project: Untitled")
        toolbar_layout.addWidget(self.project_name_label)
        
        layout.addLayout(toolbar_layout)
        
        # Main content splitter
        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # Left panel - Block type selector
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        
        # Block types group
        block_types_group = QGroupBox("Block Types")
        block_types_layout = QVBoxLayout()
        
        self.block_types_list = QListWidget()
        self.block_types_list.itemDoubleClicked.connect(self.add_block_from_list)
        block_types_layout.addWidget(self.block_types_list)
        
        # Add block button
        self.add_block_btn = QPushButton("➕ Add Selected Block")
        self.add_block_btn.clicked.connect(self.add_selected_block)
        block_types_layout.addWidget(self.add_block_btn)
        
        # Add custom block button
        self.add_custom_btn = QPushButton("➕ Add Custom Block")
        self.add_custom_btn.clicked.connect(self.add_custom_block)
        block_types_layout.addWidget(self.add_custom_btn)
        
        block_types_group.setLayout(block_types_layout)
        left_layout.addWidget(block_types_group)
        
        # Selected block properties
        properties_group = QGroupBox("Block Properties")
        properties_layout = QVBoxLayout()
        
        # Length control
        length_layout = QHBoxLayout()
        length_layout.addWidget(QLabel("Length (in):"))
        self.length_spin = QSpinBox()
        self.length_spin.setRange(1, 1000)
        self.length_spin.setValue(100)
        self.length_spin.valueChanged.connect(self.update_selected_block_size)
        length_layout.addWidget(self.length_spin)
        properties_layout.addLayout(length_layout)
        
        # Width control
        width_layout = QHBoxLayout()
        width_layout.addWidget(QLabel("Width (in):"))
        self.width_spin = QSpinBox()
        self.width_spin.setRange(1, 1000)
        self.width_spin.setValue(100)
        self.width_spin.valueChanged.connect(self.update_selected_block_size)
        width_layout.addWidget(self.width_spin)
        properties_layout.addLayout(width_layout)
        
        # Delete block button
        self.delete_block_btn = QPushButton("🗑️ Delete Block")
        self.delete_block_btn.clicked.connect(self.delete_selected_block)
        self.delete_block_btn.setEnabled(False)
        properties_layout.addWidget(self.delete_block_btn)
        
        properties_group.setLayout(properties_layout)
        left_layout.addWidget(properties_group)
        
        # Projects list
        projects_group = QGroupBox("Saved Projects")
        projects_layout = QVBoxLayout()
        
        self.projects_list = QListWidget()
        self.projects_list.itemClicked.connect(self.load_project)
        projects_layout.addWidget(self.projects_list)
        
        # Load project button
        self.load_project_btn = QPushButton("Load Selected Project")
        self.load_project_btn.clicked.connect(self.load_selected_project)
        projects_layout.addWidget(self.load_project_btn)
        
        projects_group.setLayout(projects_layout)
        left_layout.addWidget(projects_group)
        
        left_panel.setMinimumWidth(280)
        splitter.addWidget(left_panel)
        
        # Right panel - Canvas
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        
        # Canvas
        self.canvas = CanvasWidget()
        self.canvas.block_clicked.connect(self.on_block_selected)
        self.canvas.block_moved.connect(self.on_block_moved)
        right_layout.addWidget(self.canvas)
        
        # Bottom panel - Cost summary
        summary_group = QGroupBox("Cost Summary")
        summary_layout = QHBoxLayout()
        
        # Block count
        self.block_count_label = QLabel("Blocks: 0")
        summary_layout.addWidget(self.block_count_label)
        
        # Total area
        self.total_area_label = QLabel("Total Area: 0.0 sqft")
        summary_layout.addWidget(self.total_area_label)
        
        # Total cost
        self.total_cost_label = QLabel("Total Cost: $0.00")
        font = self.total_cost_label.font()
        font.setBold(True)
        font.setPointSize(14)
        self.total_cost_label.setFont(font)
        self.total_cost_label.setStyleSheet("color: #2e7d32;")
        summary_layout.addWidget(self.total_cost_label)
        
        summary_layout.addStretch()
        
        summary_group.setLayout(summary_layout)
        right_layout.addWidget(summary_group)
        
        splitter.addWidget(right_panel)
        
        # Set splitter proportions
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 3)
        
        layout.addWidget(splitter)
        
    def load_block_types(self):
        """Load block types from database."""
        self.block_types_list.clear()
        self.block_types = get_all_block_types()
        
        for block_type in self.block_types:
            item = QListWidgetItem(f"{block_type.name} (${block_type.price_per_sqft}/sqft)")
            item.setData(Qt.ItemDataRole.UserRole, block_type)
            self.block_types_list.addItem(item)
            
    def load_projects(self):
        """Load saved projects from database."""
        self.projects_list.clear()
        self.projects = get_all_projects()
        
        for project in self.projects:
            item = QListWidgetItem(f"{project.name} ({project.created_at.strftime('%Y-%m-%d')})")
            item.setData(Qt.ItemDataRole.UserRole, project)
            self.projects_list.addItem(item)
            
    def add_block_from_list(self, item):
        """Add a block from the list when double-clicked."""
        block_type = item.data(Qt.ItemDataRole.UserRole)
        if block_type:
            self.add_block(block_type)
            
    def add_selected_block(self):
        """Add the selected block type to the canvas."""
        current_item = self.block_types_list.currentItem()
        if current_item:
            block_type = current_item.data(Qt.ItemDataRole.UserRole)
            if block_type:
                self.add_block(block_type)
                
    def add_block(self, block_type):
        """Add a block of the given type to the canvas."""
        # Generate random color based on block type
        import hashlib
        hash_val = int(hashlib.md5(block_type.name.encode()).hexdigest()[:6], 16)
        color = QColor.fromRgb(
            (hash_val >> 16) & 0xFF,
            (hash_val >> 8) & 0xFF,
            hash_val & 0xFF
        )
        
        # Create new block
        block = BlockItem(
            block_type_id=block_type.id,
            name=block_type.name,
            price_per_sqft=block_type.price_per_sqft,
            length=self.length_spin.value(),
            width=self.width_spin.value(),
            x=50 + (len(self.blocks) * 20) % 300,
            y=50 + (len(self.blocks) * 20) % 300,
            color=color
        )
        
        self.blocks.append(block)
        self.canvas.add_block(block)
        self.update_cost_summary()
        
    def add_custom_block(self):
        """Add a custom block with user-defined properties."""
        # Ask for block name
        name, ok = QInputDialog.getText(self, "Add Custom Block", "Block name:")
        if not ok or not name:
            return
            
        # Ask for price per sqft
        price, ok = QInputDialog.getDouble(self, "Add Custom Block", "Price per sqft ($):", 50.0, 0.0, 10000.0, 2)
        if not ok:
            return
            
        # Create block type in database
        block_type = create_block_type(name, price)
        
        # Reload block types
        self.load_block_types()
        
        # Add the new block
        self.add_block(block_type)
        
    def on_block_selected(self, block):
        """Handle block selection."""
        self.delete_block_btn.setEnabled(True)
        self.length_spin.setValue(int(block.length))
        self.width_spin.setValue(int(block.width))
        
    def on_block_moved(self, block, x, y):
        """Handle block movement."""
        self.update_cost_summary()
        
    def update_selected_block_size(self):
        """Update the size of the selected block."""
        if self.canvas.selected_block:
            self.canvas.selected_block.length = self.length_spin.value()
            self.canvas.selected_block.width = self.width_spin.value()
            self.canvas.update()
            self.update_cost_summary()
            
    def delete_selected_block(self):
        """Delete the selected block."""
        if self.canvas.selected_block:
            self.canvas.remove_block(self.canvas.selected_block)
            if self.canvas.selected_block in self.blocks:
                self.blocks.remove(self.canvas.selected_block)
            self.canvas.selected_block = None
            self.delete_block_btn.setEnabled(False)
            self.update_cost_summary()
            
    def clear_canvas(self):
        """Clear all blocks from the canvas."""
        reply = QMessageBox.question(
            self, 'Clear Canvas', 
            'Are you sure you want to clear all blocks?',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            self.blocks = []
            self.canvas.clear_canvas()
            self.current_project_id = None
            self.current_project_name = None
            self.project_name_label.setText("Project: Untitled")
            self.update_cost_summary()
            
    def update_cost_summary(self):
        """Update the cost summary display."""
        block_count = len(self.blocks)
        total_area = sum(block.area for block in self.blocks)
        total_cost = sum(block.cost for block in self.blocks)
        
        self.block_count_label.setText(f"Blocks: {block_count}")
        self.total_area_label.setText(f"Total Area: {total_area:.1f} sqft")
        self.total_cost_label.setText(f"Total Cost: ${total_cost:,.2f}")
        
    def new_project(self):
        """Create a new project."""
        self.clear_canvas()
        
    def save_project(self):
        """Save the current project."""
        if len(self.blocks) == 0:
            QMessageBox.warning(self, "Save Project", "No blocks to save. Please add some blocks first.")
            return
            
        # Ask for project name
        name, ok = QInputDialog.getText(self, "Save Project", "Project name:", text=self.current_project_name or "My Project")
        if not ok or not name:
            return
            
        # Prepare block data
        blocks_data = [block.to_dict() for block in self.blocks]
        
        try:
            if self.current_project_id:
                # Update existing project
                project = update_project(self.current_project_id, name, blocks_data)
            else:
                # Create new project
                project = create_project(name, blocks_data)
                self.current_project_id = project.id
                
            self.current_project_name = name
            self.project_name_label.setText(f"Project: {name}")
            self.load_projects()
            
            QMessageBox.information(self, "Save Project", f"Project '{name}' saved successfully!")
            
        except Exception as e:
            QMessageBox.critical(self, "Save Project", f"Error saving project: {str(e)}")
            
    def load_selected_project(self):
        """Load the selected project."""
        current_item = self.projects_list.currentItem()
        if current_item:
            project = current_item.data(Qt.ItemDataRole.UserRole)
            self.load_project(project)
            
    def load_project(self, project):
        """Load a project from database."""
        try:
            # Get full project with blocks
            full_project = get_project(project.id)
            
            # Clear current blocks
            self.blocks = []
            self.canvas.clear_canvas()
            
            # Load blocks from project
            for block_instance in full_project.blocks.all():
                # Get block type
                block_type = block_instance.block_type
                
                # Generate color
                import hashlib
                hash_val = int(hashlib.md5(block_type.name.encode()).hexdigest()[:6], 16)
                color = QColor.fromRgb(
                    (hash_val >> 16) & 0xFF,
                    (hash_val >> 8) & 0xFF,
                    hash_val & 0xFF
                )
                
                block = BlockItem(
                    block_type_id=block_type.id,
                    name=block_type.name,
                    price_per_sqft=block_type.price_per_sqft,
                    length=block_instance.length,
                    width=block_instance.width,
                    x=block_instance.x,
                    y=block_instance.y,
                    color=color
                )
                
                self.blocks.append(block)
                self.canvas.add_block(block)
                
            self.current_project_id = full_project.id
            self.current_project_name = full_project.name
            self.project_name_label.setText(f"Project: {full_project.name}")
            self.update_cost_summary()
            
        except Exception as e:
            QMessageBox.critical(self, "Load Project", f"Error loading project: {str(e)}")
            
    def open_project(self):
        """Open project dialog."""
        self.load_projects()
        
    def refresh(self):
        """Refresh the calculator tab."""
        self.load_block_types()
        self.load_projects()
