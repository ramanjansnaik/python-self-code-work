"""
Test Generator tab for the PyQt6 Desktop Application.
Provides AI-powered test generation functionality.
"""
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
    QLineEdit, QTextEdit, QListWidget, QListWidgetItem, QGroupBox,
    QComboBox, QSpinBox, QMessageBox, QDialog, QDialogButtonBox,
    QFormLayout, QSplitter, QProgressBar, QScrollArea, QFrame,
    QTableWidget, QTableWidgetItem, QHeaderView, QTabWidget
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QTimer
from PyQt6.QtGui import QFont, QColor

from desktop_app.database import (
    get_all_llm_providers, create_llm_provider,
    get_all_test_projects, create_test_project,
    get_all_generated_tests, create_generated_test
)


class TestGenerationWorker(QThread):
    """Worker thread for generating tests."""
    
    progress = pyqtSignal(str)
    finished = pyqtSignal(str)
    error = pyqtSignal(str)
    
    def __init__(self, website_url, framework, language, api_key=None):
        super().__init__()
        self.website_url = website_url
        self.framework = framework
        self.language = language
        self.api_key = api_key
        
    def run(self):
        """Run the test generation."""
        try:
            self.progress.emit("Analyzing website...")
            
            # Simulate website analysis
            import time
            time.sleep(1)
            
            self.progress.emit("Generating test scenarios...")
            time.sleep(1)
            
            # Generate sample test code
            test_code = self._generate_sample_test()
            
            self.progress.emit("Test generation complete!")
            self.finished.emit(test_code)
            
        except Exception as e:
            self.error.emit(str(e))
            
    def _generate_sample_test(self):
        """Generate sample test code based on framework and language."""
        
        if self.framework == 'playwright':
            if self.language == 'python':
                return '''"""Generated Playwright tests."""
import pytest
from playwright.sync_api import Page, expect


def test_homepage_loads(page: Page):
    """Test that the homepage loads successfully."""
    page.goto("''' + self.website_url + '''")
    expect(page).to_have_title(/.*/)
    
    
def test_navigation_menu(page: Page):
    """Test navigation menu functionality."""
    page.goto("''' + self.website_url + '''")
    # Add navigation tests here
    
    
def test_form_submission(page: Page):
    """Test form submission."""
    page.goto("''' + self.website_url + '''")
    # Add form tests here
'''
            elif self.language == 'javascript':
                return '''const { test, expect } = require('@playwright/test');

test('homepage loads', async ({ page }) => {
  await page.goto('''' + self.website_url + '''');
  await expect(page).toHaveTitle(/.*/);
});

test('navigation menu', async ({ page }) => {
  await page.goto('''' + self.website_url + '''');
  // Add navigation tests
});
'''
        elif self.framework == 'selenium':
            if self.language == 'python':
                return '''"""Generated Selenium tests."""
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pytest


def test_homepage_loads():
    """Test that the homepage loads successfully."""
    driver = webdriver.Chrome()
    driver.get("''' + self.website_url + '''")
    assert "''' + self.website_url + '''" in driver.current_url
    driver.quit()
    
    
def test_navigation():
    """Test navigation menu functionality."""
    driver = webdriver.Chrome()
    driver.get("''' + self.website_url + '''")
    # Add navigation tests
    driver.quit()
'''
        return "# No test template available for this combination"


class TestGenTab(QWidget):
    """Tab widget for test generation functionality."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.main_window = parent
        self.current_llm_provider = None
        self.test_projects = []
        self.generated_tests = []
        self.init_ui()
        self.load_data()
        
    def init_ui(self):
        """Initialize the user interface."""
        layout = QVBoxLayout(self)
        
        # Header
        header_layout = QHBoxLayout()
        
        title_label = QLabel("🧪 AI-Powered Test Generator")
        font = title_label.font()
        font.setPointSize(16)
        font.setBold(True)
        title_label.setFont(font)
        header_layout.addWidget(title_label)
        
        header_layout.addStretch()
        
        # Refresh button
        self.refresh_btn = QPushButton("🔄 Refresh")
        self.refresh_btn.clicked.connect(self.load_data)
        header_layout.addWidget(self.refresh_btn)
        
        layout.addLayout(header_layout)
        
        # Main splitter
        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # Left panel - Projects and Providers
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        
        # LLM Providers group
        llm_group = QGroupBox("LLM Providers")
        llm_layout = QVBoxLayout()
        
        self.llm_providers_list = QListWidget()
        self.llm_providers_list.itemClicked.connect(self.on_llm_provider_selected)
        llm_layout.addWidget(self.llm_providers_list)
        
        # Add provider button
        self.add_provider_btn = QPushButton("➕ Add Provider")
        self.add_provider_btn.clicked.connect(self.add_llm_provider)
        llm_layout.addWidget(self.add_provider_btn)
        
        llm_group.setLayout(llm_layout)
        left_layout.addWidget(llm_group)
        
        # Test Projects group
        projects_group = QGroupBox("Test Projects")
        projects_layout = QVBoxLayout()
        
        self.test_projects_list = QListWidget()
        self.test_projects_list.itemClicked.connect(self.on_test_project_selected)
        projects_layout.addWidget(self.test_projects_list)
        
        # Add project button
        self.add_project_btn = QPushButton("➕ New Test Project")
        self.add_project_btn.clicked.connect(self.add_test_project)
        projects_layout.addWidget(self.add_project_btn)
        
        projects_group.setLayout(projects_layout)
        left_layout.addWidget(projects_group)
        
        left_panel.setMinimumWidth(300)
        splitter.addWidget(left_panel)
        
        # Right panel - Test Generation
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        
        # Test generation form
        generation_group = QGroupBox("Generate New Tests")
        generation_layout = QFormLayout()
        
        # Website URL
        self.website_url_input = QLineEdit()
        self.website_url_input.setPlaceholderText("https://example.com")
        generation_layout.addRow("Website URL:", self.website_url_input)
        
        # Framework selection
        self.framework_combo = QComboBox()
        self.framework_combo.addItems(["Playwright", "Selenium"])
        generation_layout.addRow("Framework:", self.framework_combo)
        
        # Language selection
        self.language_combo = QComboBox()
        self.language_combo.addItems(["Python", "JavaScript", "TypeScript", "Java", "C#"])
        generation_layout.addRow("Language:", self.language_combo)
        
        # API Key (optional)
        self.api_key_input = QLineEdit()
        self.api_key_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.api_key_input.setPlaceholderText("Optional: API Key for enhanced generation")
        generation_layout.addRow("API Key:", self.api_key_input)
        
        # Generate button
        self.generate_btn = QPushButton("🚀 Generate Tests")
        self.generate_btn.clicked.connect(self.generate_tests)
        generation_layout.addRow("", self.generate_btn)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        generation_layout.addRow("Progress:", self.progress_bar)
        
        generation_group.setLayout(generation_layout)
        right_layout.addWidget(generation_group)
        
        # Generated tests display
        tests_group = QGroupBox("Generated Tests")
        tests_layout = QVBoxLayout()
        
        # Test output
        self.test_output = QTextEdit()
        self.test_output.setReadOnly(True)
        self.test_output.setFont(QFont("Courier New", 10))
        self.test_output.setPlaceholderText("Generated tests will appear here...")
        tests_layout.addWidget(self.test_output)
        
        # Test actions
        test_actions_layout = QHBoxLayout()
        
        self.save_test_btn = QPushButton("💾 Save Test")
        self.save_test_btn.clicked.connect(self.save_test)
        self.save_test_btn.setEnabled(False)
        test_actions_layout.addWidget(self.save_test_btn)
        
        self.copy_test_btn = QPushButton("📋 Copy to Clipboard")
        self.copy_test_btn.clicked.connect(self.copy_test)
        test_actions_layout.addWidget(self.copy_test_btn)
        
        test_actions_layout.addStretch()
        
        tests_layout.addLayout(test_actions_layout)
        
        tests_group.setLayout(tests_layout)
        right_layout.addWidget(tests_group)
        
        splitter.addWidget(right_panel)
        
        # Set splitter proportions
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 2)
        
        layout.addWidget(splitter)
        
    def load_data(self):
        """Load all data from database."""
        self.load_llm_providers()
        self.load_test_projects()
        self.load_generated_tests()
        
    def load_llm_providers(self):
        """Load LLM providers from database."""
        self.llm_providers_list.clear()
        self.llm_providers = get_all_llm_providers()
        
        for provider in self.llm_providers:
            item = QListWidgetItem(f"{provider.name} ({provider.provider_type})")
            item.setData(Qt.ItemDataRole.UserRole, provider)
            self.llm_providers_list.addItem(item)
            
    def load_test_projects(self):
        """Load test projects from database."""
        self.test_projects_list.clear()
        self.test_projects = get_all_test_projects()
        
        for project in self.test_projects:
            item = QListWidgetItem(f"{project.name} ({project.framework})")
            item.setData(Qt.ItemDataRole.UserRole, project)
            self.test_projects_list.addItem(item)
            
    def load_generated_tests(self):
        """Load generated tests from database."""
        self.generated_tests = get_all_generated_tests()
        
    def on_llm_provider_selected(self, item):
        """Handle LLM provider selection."""
        provider = item.data(Qt.ItemDataRole.UserRole)
        self.current_llm_provider = provider
        
    def on_test_project_selected(self, item):
        """Handle test project selection."""
        project = item.data(Qt.ItemDataRole.UserRole)
        # Could load project-specific tests here
        
    def add_llm_provider(self):
        """Add a new LLM provider."""
        dialog = LLMProviderDialog(self)
        if dialog.exec():
            provider_data = dialog.get_provider_data()
            try:
                provider = create_llm_provider(
                    name=provider_data['name'],
                    provider_type=provider_data['provider_type'],
                    api_endpoint=provider_data['api_endpoint'],
                    api_key=provider_data['api_key'],
                    model_name=provider_data['model_name']
                )
                self.load_llm_providers()
                QMessageBox.information(self, "Success", f"Provider '{provider.name}' created successfully!")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to create provider: {str(e)}")
                
    def add_test_project(self):
        """Add a new test project."""
        dialog = TestProjectDialog(self, self.llm_providers)
        if dialog.exec():
            project_data = dialog.get_project_data()
            try:
                project = create_test_project(
                    name=project_data['name'],
                    description=project_data['description'],
                    website_url=project_data['website_url'],
                    framework=project_data['framework'],
                    language=project_data['language'],
                    llm_provider_id=project_data['llm_provider_id']
                )
                self.load_test_projects()
                QMessageBox.information(self, "Success", f"Test project '{project.name}' created successfully!")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to create test project: {str(e)}")
                
    def generate_tests(self):
        """Generate tests using AI."""
        website_url = self.website_url_input.text().strip()
        
        if not website_url:
            QMessageBox.warning(self, "Input Error", "Please enter a website URL.")
            return
            
        # Validate URL
        if not website_url.startswith(('http://', 'https://')):
            QMessageBox.warning(self, "Input Error", "Please enter a valid URL starting with http:// or https://")
            return
            
        framework = self.framework_combo.currentText().lower()
        language = self.language_combo.currentText().lower()
        api_key = self.api_key_input.text().strip() or None
        
        # Disable generate button and show progress
        self.generate_btn.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 0)  # Indeterminate progress
        
        # Create worker thread
        self.worker = TestGenerationWorker(website_url, framework, language, api_key)
        self.worker.progress.connect(self.on_generation_progress)
        self.worker.finished.connect(self.on_generation_finished)
        self.worker.error.connect(self.on_generation_error)
        self.worker.start()
        
    def on_generation_progress(self, message):
        """Handle generation progress."""
        self.progress_bar.setFormat(message)
        
    def on_generation_finished(self, test_code):
        """Handle generation completion."""
        self.progress_bar.setVisible(False)
        self.generate_btn.setEnabled(True)
        
        self.generated_test_code = test_code
        self.test_output.setPlainText(test_code)
        self.save_test_btn.setEnabled(True)
        
        QMessageBox.information(self, "Success", "Tests generated successfully!")
        
    def on_generation_error(self, error):
        """Handle generation error."""
        self.progress_bar.setVisible(False)
        self.generate_btn.setEnabled(True)
        
        QMessageBox.critical(self, "Error", f"Failed to generate tests: {error}")
        
    def save_test(self):
        """Save the generated test."""
        test_code = self.test_output.toPlainText()
        
        if not test_code:
            QMessageBox.warning(self, "Save Error", "No test to save.")
            return
            
        # Get test project (or create new)
        project_item = self.test_projects_list.currentItem()
        
        if not project_item:
            QMessageBox.warning(self, "Save Error", "Please select or create a test project first.")
            return
            
        test_project = project_item.data(Qt.ItemDataRole.UserRole)
        
        # Ask for test name and filename
        test_name, ok1 = QInputDialog.getText(self, "Save Test", "Test name:", text="Test Homepage")
        if not ok1 or not test_name:
            return
            
        file_name, ok2 = QInputDialog.getText(self, "Save Test", "File name:", text="test_homepage.py")
        if not ok2 or not file_name:
            return
            
        try:
            test = create_generated_test(
                test_project_id=test_project.id,
                test_name=test_name,
                test_description="",
                test_code=test_code,
                file_name=file_name
            )
            
            self.load_generated_tests()
            QMessageBox.information(self, "Success", f"Test '{test.test_name}' saved successfully!")
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save test: {str(e)}")
            
    def copy_test(self):
        """Copy test code to clipboard."""
        test_code = self.test_output.toPlainText()
        
        if test_code:
            clipboard = self.clipboard()
            from PyQt6.QtWidgets import QApplication
            QApplication.clipboard().setText(test_code)
            QMessageBox.information(self, "Copied", "Test code copied to clipboard!")
        else:
            QMessageBox.warning(self, "Copy Error", "No test to copy.")


class LLMProviderDialog(QDialog):
    """Dialog for adding/editing LLM providers."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add LLM Provider")
        self.init_ui()
        
    def init_ui(self):
        """Initialize the dialog UI."""
        layout = QFormLayout(self)
        
        # Name
        self.name_input = QLineEdit()
        layout.addRow("Name:", self.name_input)
        
        # Provider type
        self.type_combo = QComboBox()
        self.type_combo.addItems(["openai", "anthropic", "google", "ollama", "custom"])
        layout.addRow("Provider Type:", self.type_combo)
        
        # API Endpoint
        self.endpoint_input = QLineEdit()
        self.endpoint_input.setPlaceholderText("https://api.openai.com/v1")
        layout.addRow("API Endpoint:", self.endpoint_input)
        
        # API Key
        self.api_key_input = QLineEdit()
        self.api_key_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addRow("API Key:", self.api_key_input)
        
        # Model name
        self.model_input = QLineEdit()
        self.model_input.setText("gpt-4")
        layout.addRow("Model Name:", self.model_input)
        
        # Buttons
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addRow("", buttons)
        
    def get_provider_data(self):
        """Get the provider data from the form."""
        return {
            'name': self.name_input.text().strip(),
            'provider_type': self.type_combo.currentText(),
            'api_endpoint': self.endpoint_input.text().strip(),
            'api_key': self.api_key_input.text().strip() or None,
            'model_name': self.model_input.text().strip()
        }


class TestProjectDialog(QDialog):
    """Dialog for adding test projects."""
    
    def __init__(self, parent=None, llm_providers=None):
        super().__init__(parent)
        self.llm_providers = llm_providers or []
        self.setWindowTitle("New Test Project")
        self.init_ui()
        
    def init_ui(self):
        """Initialize the dialog UI."""
        layout = QFormLayout(self)
        
        # Name
        self.name_input = QLineEdit()
        layout.addRow("Project Name:", self.name_input)
        
        # Description
        self.description_input = QTextEdit()
        self.description_input.setMaximumHeight(80)
        layout.addRow("Description:", self.description_input)
        
        # Website URL
        self.website_input = QLineEdit()
        self.website_input.setPlaceholderText("https://example.com")
        layout.addRow("Website URL:", self.website_input)
        
        # Framework
        self.framework_combo = QComboBox()
        self.framework_combo.addItems(["playwright", "selenium"])
        layout.addRow("Framework:", self.framework_combo)
        
        # Language
        self.language_combo = QComboBox()
        self.language_combo.addItems(["python", "javascript", "typescript", "java", "csharp"])
        layout.addRow("Language:", self.language_combo)
        
        # LLM Provider
        self.provider_combo = QComboBox()
        self.provider_combo.addItem("None", None)
        for provider in self.llm_providers:
            self.provider_combo.addItem(provider.name, provider.id)
        layout.addRow("LLM Provider:", self.provider_combo)
        
        # Buttons
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addRow("", buttons)
        
    def get_project_data(self):
        """Get the project data from the form."""
        return {
            'name': self.name_input.text().strip(),
            'description': self.description_input.toPlainText().strip(),
            'website_url': self.website_input.text().strip(),
            'framework': self.framework_combo.currentText(),
            'language': self.language_combo.currentText(),
            'llm_provider_id': self.provider_combo.currentData()
        }
