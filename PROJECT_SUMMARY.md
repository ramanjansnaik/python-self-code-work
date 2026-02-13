# TestGen - Project Summary

## Overview

TestGen is a full-stack AI-powered test generation platform that automatically generates executable Playwright and Selenium test cases using configurable LLM APIs (OpenAI, Anthropic, Google, Ollama) and creates CI/CD pipeline configurations.

## Architecture

### Backend (Django + DRF)
- **Framework**: Django 5.2.4 with Django REST Framework 3.15.2
- **Database**: SQLite (default), easily configurable for PostgreSQL/MySQL
- **API**: RESTful API with viewsets and routers
- **Authentication**: Session-based authentication
- **CORS**: Enabled for React frontend communication

### Frontend (React)
- **Framework**: React 18.2 with React Router 6
- **HTTP Client**: Axios with CSRF token handling
- **Styling**: Modern CSS with gradient designs
- **State Management**: React hooks (useState, useEffect)

## Key Features

### 1. LLM Provider Management
- Support for multiple LLM providers:
  - OpenAI (GPT-4, GPT-3.5-turbo)
  - Anthropic (Claude)
  - Google (Gemini)
  - Ollama (local models)
  - Custom API endpoints
- Secure API key storage
- Provider activation/deactivation

### 2. Test Project Management
- Create projects with:
  - Website URL
  - Test framework (Playwright/Selenium)
  - Programming language (Python, JavaScript, TypeScript, Java, C#)
  - LLM provider selection
- Server configuration for multiple environments
- Project-level metadata and tracking

### 3. AI-Powered Test Generation
- Natural language test scenario input
- Automatic test code generation
- Configurable options:
  - Browser selection (Chromium, Firefox, WebKit)
  - Headless mode
  - Timeout settings
  - Setup/teardown inclusion
- Real-time generation status tracking
- Error handling and retry capabilities

### 4. CI/CD Pipeline Generation
- Automatic GitHub Actions configuration
- Automatic GitLab CI configuration
- Configurable triggers:
  - Push events
  - Pull request events
  - Cron schedules
- Framework and language-specific configurations

### 5. Test Management
- View all generated tests
- Download individual or all tests
- Regenerate failed tests
- Track generation time and status
- Store LLM prompts and responses

## Data Models

### LLMProvider
- Provider type, name, endpoint
- API credentials
- Model configuration
- User association

### TestProject
- Project metadata
- Framework and language selection
- LLM provider link
- User association

### ServerConfig
- Hostname, port, protocol
- Authentication details
- Environment variables
- Multiple configs per project

### GeneratedTest
- Test code and metadata
- Generation status
- Performance metrics
- LLM interaction logs

### CICDPipeline
- Pipeline provider
- Configuration content
- Trigger settings
- One-to-one with TestProject

## API Endpoints

### LLM Providers
- `GET /api/testgen/llm-providers/` - List all providers
- `POST /api/testgen/llm-providers/` - Create new provider
- `GET /api/testgen/llm-providers/{id}/` - Get provider details
- `PUT /api/testgen/llm-providers/{id}/` - Update provider
- `DELETE /api/testgen/llm-providers/{id}/` - Delete provider

### Projects
- `GET /api/testgen/projects/` - List all projects
- `POST /api/testgen/projects/` - Create new project
- `GET /api/testgen/projects/{id}/` - Get project details
- `PUT /api/testgen/projects/{id}/` - Update project
- `DELETE /api/testgen/projects/{id}/` - Delete project
- `POST /api/testgen/projects/{id}/generate_tests/` - Generate tests
- `POST /api/testgen/projects/{id}/generate_cicd/` - Generate CI/CD
- `GET /api/testgen/projects/{id}/download_tests/` - Download all tests

### Server Configs
- `GET /api/testgen/server-configs/` - List configs
- `POST /api/testgen/server-configs/` - Create config
- `DELETE /api/testgen/server-configs/{id}/` - Delete config

### Generated Tests
- `GET /api/testgen/generated-tests/` - List tests
- `GET /api/testgen/generated-tests/{id}/` - Get test details
- `POST /api/testgen/generated-tests/{id}/regenerate/` - Regenerate test

### CI/CD Pipelines
- `GET /api/testgen/cicd-pipelines/` - List pipelines
- `GET /api/testgen/cicd-pipelines/{id}/` - Get pipeline details

## Service Layer

### LLMService
- Unified interface for multiple LLM providers
- Provider-specific completion methods
- Error handling and retry logic
- Token usage tracking

### TestGeneratorService
- Test scenario to code conversion
- Prompt engineering
- Code extraction from LLM responses
- File naming conventions

### CICDGeneratorService
- Framework and language-specific templates
- GitHub Actions YAML generation
- GitLab CI YAML generation
- Configurable triggers and schedules

## Frontend Pages

### Dashboard
- Statistics overview
- Recent projects
- Quick actions
- Getting started guide

### LLM Providers
- Provider list with management
- Add/edit/delete providers
- Provider configuration forms

### Projects
- Project list with filtering
- Project cards with metadata
- Quick actions per project

### Create Project
- Multi-step form
- Server configuration builder
- Validation and error handling

### Project Detail
- Test generation interface
- Generated tests list
- CI/CD pipeline configuration
- Download capabilities

## Installation Methods

### 1. Automated Script
```bash
./install.sh
```

### 2. Manual Installation
```bash
# Backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate

# Frontend
cd frontend
npm install
```

### 3. Docker Compose
```bash
docker-compose up
```

## Configuration

### Environment Variables
- `SECRET_KEY` - Django secret key
- `DEBUG` - Debug mode (True/False)
- `ALLOWED_HOSTS` - Comma-separated host list
- `CORS_ALLOWED_ORIGINS` - Frontend origins

### Database
- Default: SQLite (development)
- Production: PostgreSQL recommended
- Easily configurable in settings.py

## Security Features

- CSRF protection on all POST requests
- Session-based authentication
- API key encryption (write-only)
- SSH key encryption (write-only)
- CORS restrictions
- Environment variable configuration

## Deployment

### Development
```bash
# Backend
python manage.py runserver

# Frontend
cd frontend && npm start
```

### Production
- Use gunicorn for Django
- Build React app: `npm run build`
- Serve with nginx/Apache
- Configure production database
- Set environment variables
- Disable DEBUG mode

## Testing

### Backend
```bash
python manage.py test
```

### Frontend
```bash
cd frontend && npm test
```

## Future Enhancements

1. More test frameworks (Cypress, TestCafe)
2. Test execution and reporting
3. Integration with test management tools
4. Multi-user collaboration
5. Docker deployment templates
6. Kubernetes manifests
7. More CI/CD providers
8. Visual test recorder
9. Test analytics and insights
10. Scheduled test generation

## Technology Stack Summary

**Backend:**
- Python 3.11+
- Django 5.2.4
- Django REST Framework 3.15.2
- django-cors-headers 4.3.1
- requests 2.31.0
- gunicorn 21.2.0
- SQLite/PostgreSQL

**Frontend:**
- Node.js 18+
- React 18.2
- React Router 6
- Axios 1.6
- Modern CSS

**DevOps:**
- Docker & Docker Compose
- GitHub Actions
- GitLab CI
- Nginx (production)

## File Structure

```
precostcalc/
├── calculator/              # Original calculator app
├── precostcalc/            # Django project settings
│   ├── settings.py         # Configuration
│   ├── urls.py             # URL routing
│   └── wsgi.py             # WSGI config
├── testgen/                # Test generation app
│   ├── models.py           # Data models
│   ├── views.py            # API views
│   ├── serializers.py      # DRF serializers
│   ├── services.py         # Business logic
│   ├── urls.py             # API routes
│   └── admin.py            # Admin interface
├── frontend/               # React frontend
│   ├── public/             # Static files
│   ├── src/
│   │   ├── pages/          # Page components
│   │   ├── services/       # API client
│   │   ├── App.js          # Main app
│   │   └── index.js        # Entry point
│   └── package.json        # Dependencies
├── requirements.txt        # Python dependencies
├── manage.py              # Django CLI
├── install.sh             # Installation script
├── README.md              # Documentation
├── QUICKSTART.md          # Quick start guide
├── CONTRIBUTING.md        # Contribution guide
└── docker-compose.yml     # Docker configuration
```

## License

MIT License - See LICENSE file for details.

## Support

For issues, questions, or contributions:
- Check documentation files
- Review existing issues
- Create new issues on GitHub
- Submit pull requests

---

Built with ❤️ using Django, React, and modern LLM APIs.
