# Contributing to TestGen

Thank you for considering contributing to TestGen! This document provides guidelines and instructions for contributing.

## Getting Started

1. Fork the repository
2. Clone your fork:
   ```bash
   git clone https://github.com/yourusername/testgen.git
   cd testgen
   ```
3. Install dependencies:
   ```bash
   ./install.sh
   ```

## Development Setup

### Backend Development

```bash
# Activate virtual environment
source .venv/bin/activate

# Install development dependencies
pip install black flake8 pytest pytest-django

# Run tests
python manage.py test

# Format code
black .

# Lint code
flake8
```

### Frontend Development

```bash
cd frontend

# Install dependencies
npm install

# Run tests
npm test

# Lint code
npm run lint

# Format code
npm run format
```

## Making Changes

1. Create a new branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Make your changes

3. Test your changes:
   ```bash
   # Backend
   python manage.py test
   
   # Frontend
   cd frontend && npm test
   ```

4. Commit your changes:
   ```bash
   git add .
   git commit -m "feat: add your feature description"
   ```

## Commit Message Format

We follow the Conventional Commits specification:

- `feat:` - A new feature
- `fix:` - A bug fix
- `docs:` - Documentation changes
- `style:` - Code style changes (formatting, etc.)
- `refactor:` - Code refactoring
- `test:` - Adding or updating tests
- `chore:` - Maintenance tasks

Examples:
```
feat: add support for Cypress framework
fix: resolve CORS issue with frontend
docs: update installation instructions
```

## Pull Request Process

1. Update the README.md with details of changes if applicable
2. Update the CHANGELOG.md with your changes
3. Ensure all tests pass
4. Update documentation as needed
5. Submit a pull request with a clear description

## Code Style

### Python (Backend)
- Follow PEP 8
- Use Black for formatting
- Maximum line length: 100 characters
- Use type hints where appropriate
- Write docstrings for functions and classes

### JavaScript/React (Frontend)
- Follow Airbnb JavaScript Style Guide
- Use ES6+ features
- Use functional components with hooks
- Write meaningful component and variable names
- Add comments for complex logic

## Testing

### Backend Tests

```python
# tests.py
from django.test import TestCase
from .models import TestProject

class TestProjectTestCase(TestCase):
    def test_project_creation(self):
        project = TestProject.objects.create(
            name="Test Project",
            website_url="https://example.com",
            framework="playwright",
            language="python"
        )
        self.assertEqual(project.name, "Test Project")
```

### Frontend Tests

```javascript
// Component.test.js
import { render, screen } from '@testing-library/react';
import Component from './Component';

test('renders component', () => {
  render(<Component />);
  expect(screen.getByText(/expected text/i)).toBeInTheDocument();
});
```

## Adding New Features

### Adding a New LLM Provider

1. Update `testgen/models.py`:
   - Add provider to `PROVIDER_CHOICES`

2. Update `testgen/services.py`:
   - Add `_provider_completion` method to `LLMService`

3. Update `frontend/src/pages/LLMProviders.js`:
   - Add provider to form options

4. Test the integration

### Adding a New Test Framework

1. Update `testgen/models.py`:
   - Add framework to `FRAMEWORK_CHOICES`

2. Update `testgen/services.py`:
   - Add framework-specific prompt template
   - Add CI/CD configuration template

3. Update frontend forms

4. Test test generation

## Documentation

- Update README.md for major features
- Add inline code comments for complex logic
- Update API documentation
- Add examples for new features

## Issue Reporting

When reporting issues, please include:

- Operating system and version
- Python and Node.js versions
- Steps to reproduce
- Expected behavior
- Actual behavior
- Screenshots (if applicable)
- Error messages and stack traces

## Feature Requests

Feature requests are welcome! Please:

- Check if the feature already exists
- Clearly describe the feature
- Explain the use case
- Provide examples if possible

## Code Review

All submissions require review. We use GitHub pull requests for this purpose.

Reviewers will check:
- Code quality and style
- Test coverage
- Documentation
- Performance implications
- Security considerations

## Community

- Be respectful and inclusive
- Help others learn and grow
- Share knowledge and best practices
- Provide constructive feedback

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

## Questions?

If you have questions about contributing, please:
- Check existing documentation
- Search closed issues
- Open a new issue with the "question" label

Thank you for contributing to TestGen! 🚀
