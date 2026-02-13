"""
Database module for PyQt6 Desktop Application.
Provides direct access to Django models without REST API.
"""
import os
import sys

# Add project directory to path
project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_dir)

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'precostcalc.settings')

import django
django.setup()

from django.contrib.auth.models import User
from calculator.models import BlockType, Project, BlockInstance
from testgen.models import LLMProvider, TestProject, ServerConfig, GeneratedTest, CICDPipeline


def init_database():
    """Initialize database connection and create default data."""
    # Ensure database is migrated
    from django.core.management import execute_from_command_line
    try:
        execute_from_command_line(['manage.py', 'migrate', '--run-syncdb'])
    except Exception as e:
        print(f"Database migration: {e}")
    
    # Create default block types if none exist
    if BlockType.objects.count() == 0:
        default_blocks = [
            {'name': 'Standard Room', 'price_per_sqft': 50.00},
            {'name': 'Premium Room', 'price_per_sqft': 75.00},
            {'name': 'Bathroom', 'price_per_sqft': 100.00},
            {'name': 'Kitchen', 'price_per_sqft': 120.00},
            {'name': 'Garage', 'price_per_sqft': 35.00},
        ]
        for block in default_blocks:
            BlockType.objects.create(**block)
    
    # Create default user if none exist
    if User.objects.count() == 0:
        User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    
    return True


# Block Type operations
def get_all_block_types():
    """Get all block types."""
    return list(BlockType.objects.all())


def create_block_type(name, price_per_sqft):
    """Create a new block type."""
    return BlockType.objects.create(name=name, price_per_sqft=price_per_sqft)


def update_block_type(block_type_id, name=None, price_per_sqft=None):
    """Update a block type."""
    block_type = BlockType.objects.get(id=block_type_id)
    if name is not None:
        block_type.name = name
    if price_per_sqft is not None:
        block_type.price_per_sqft = price_per_sqft
    block_type.save()
    return block_type


def delete_block_type(block_type_id):
    """Delete a block type."""
    BlockType.objects.get(id=block_type_id).delete()


# Project operations
def get_all_projects():
    """Get all projects."""
    return list(Project.objects.all().order_by('-created_at'))


def get_project(project_id):
    """Get a single project with its blocks."""
    return Project.objects.prefetch_related('blocks').get(id=project_id)


def create_project(name, blocks_data):
    """Create a new project with block instances."""
    # Get or create admin user
    user, _ = User.objects.get_or_create(username='admin')
    
    project = Project.objects.create(name=name, created_by=user)
    
    for block_data in blocks_data:
        BlockInstance.objects.create(
            project=project,
            block_type_id=block_data['block_type_id'],
            length=block_data.get('length', 10),
            width=block_data.get('width', 10),
            x=block_data.get('x', 0),
            y=block_data.get('y', 0)
        )
    
    return project


def update_project(project_id, name=None, blocks_data=None):
    """Update a project."""
    project = Project.objects.get(id=project_id)
    
    if name is not None:
        project.name = name
    
    if blocks_data is not None:
        # Delete existing blocks and create new ones
        project.blocks.all().delete()
        for block_data in blocks_data:
            BlockInstance.objects.create(
                project=project,
                block_type_id=block_data['block_type_id'],
                length=block_data.get('length', 10),
                width=block_data.get('width', 10),
                x=block_data.get('x', 0),
                y=block_data.get('y', 0)
            )
    
    project.save()
    return project


def delete_project(project_id):
    """Delete a project."""
    Project.objects.get(id=project_id).delete()


# TestGen operations
def get_all_llm_providers():
    """Get all LLM providers."""
    return list(LLMProvider.objects.all())


def create_llm_provider(name, provider_type, api_endpoint, api_key, model_name):
    """Create a new LLM provider."""
    user, _ = User.objects.get_or_create(username='admin')
    return LLMProvider.objects.create(
        name=name,
        provider_type=provider_type,
        api_endpoint=api_endpoint,
        api_key=api_key,
        model_name=model_name,
        created_by=user
    )


def get_all_test_projects():
    """Get all test projects."""
    return list(TestProject.objects.all())


def create_test_project(name, description, website_url, framework, language, llm_provider_id):
    """Create a new test project."""
    user, _ = User.objects.get_or_create(username='admin')
    llm_provider = LLMProvider.objects.get(id=llm_provider_id) if llm_provider_id else None
    return TestProject.objects.create(
        name=name,
        description=description,
        website_url=website_url,
        framework=framework,
        language=language,
        llm_provider=llm_provider,
        created_by=user
    )


def get_all_generated_tests():
    """Get all generated tests."""
    return list(GeneratedTest.objects.all())


def create_generated_test(test_project_id, test_name, test_description, test_code, file_name):
    """Create a new generated test."""
    test_project = TestProject.objects.get(id=test_project_id)
    return GeneratedTest.objects.create(
        test_project=test_project,
        test_name=test_name,
        test_description=test_description,
        test_code=test_code,
        file_name=file_name,
        status='completed'
    )
