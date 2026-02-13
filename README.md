# TestGen - AI-Powered Test Generation Platform

A full-stack web application that generates executable Playwright and Selenium test cases using configurable LLM APIs, with automatic GitHub Actions CI/CD pipeline configuration.

## Features

- 🤖 **AI-Powered Test Generation**: Generate executable test cases using OpenAI, Anthropic, Google, or local Ollama models
- 🎯 **Multi-Framework Support**: Generate tests for Playwright or Selenium
- 💻 **Multi-Language Support**: Python, JavaScript, TypeScript, Java, and C#
- 🔧 **Server Configuration**: Support for multiple test environments
- 🚀 **CI/CD Integration**: Automatic generation of GitHub Actions and GitLab CI pipeline configurations
- 📦 **Locally Installable**: Easy setup and deployment
- 🎨 **Modern React Frontend**: Clean, responsive UI built with React

## Tech Stack

### Backend
- Django 5.2.4
- Django REST Framework 3.15.2
- SQLite (default, easily swappable)
- Python 3.11+

### Frontend
- React 18.2
- React Router 6
- Axios for API calls
- Modern CSS with gradient designs

## Installation

### Prerequisites
- Python 3.11 or higher
- Node.js 18 or higher
- npm or yarn

### Backend Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd precostcalc
```

2. Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install Python dependencies:
```bash
pip install -r requirements.txt
```

4. Run migrations:
```bash
python manage.py migrate
```

5. Create a superuser:
```bash
python manage.py createsuperuser
```

6. Start the Django development server:
```bash
python manage.py runserver
```

The backend API will be available at `http://localhost:8000`

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the React development server:
```bash
npm start
```

The frontend will be available at `http://localhost:3000`

## Usage

### 1. Configure LLM Provider

Before generating tests, you need to configure at least one LLM provider:

1. Navigate to **LLM Providers** in the navigation menu
2. Click **Add Provider**
3. Fill in the details:
   - **OpenAI**: Use `https://api.openai.com/v1` with your API key
   - **Anthropic**: Use `https://api.anthropic.com/v1` with your API key
   - **Google**: Use the Gemini API endpoint with your API key
   - **Ollama (Local)**: Use `http://localhost:11434` (no API key needed)
   - **Custom API**: Configure your own endpoint

### 2. Create a Test Project

1. Navigate to **Projects** → **Create Project**
2. Fill in project details:
   - Project name and description
   - Website URL to test
   - Choose framework (Playwright or Selenium)
   - Choose programming language
   - Select LLM provider
3. Optionally add server configurations for specific environments
4. Click **Create Project**

### 3. Generate Tests

1. Open your project
2. In the **Generate Tests** section:
   - Add test scenarios (e.g., "Test user login with valid credentials")
   - Configure test options (browser, timeout, headless mode)
   - Click **Generate Tests**
3. Wait for AI to generate your test code
4. Download individual tests or all tests at once

### 4. Generate CI/CD Pipeline

1. In the project detail page, scroll to **CI/CD Pipeline Configuration**
2. Choose your CI/CD provider (GitHub Actions or GitLab CI)
3. Configure pipeline options (triggers, schedule)
4. Click **Generate Pipeline**
5. Download the pipeline configuration file and add it to your repository

## API Endpoints

### LLM Providers
- `GET /api/testgen/llm-providers/` - List providers
- `POST /api/testgen/llm-providers/` - Create provider
- `GET /api/testgen/llm-providers/{id}/` - Get provider
- `PUT /api/testgen/llm-providers/{id}/` - Update provider
- `DELETE /api/testgen/llm-providers/{id}/` - Delete provider

### Projects
- `GET /api/testgen/projects/` - List projects
- `POST /api/testgen/projects/` - Create project
- `GET /api/testgen/projects/{id}/` - Get project
- `PUT /api/testgen/projects/{id}/` - Update project
- `DELETE /api/testgen/projects/{id}/` - Delete project
- `POST /api/testgen/projects/{id}/generate_tests/` - Generate tests
- `POST /api/testgen/projects/{id}/generate_cicd/` - Generate CI/CD config
- `GET /api/testgen/projects/{id}/download_tests/` - Download all tests

### Generated Tests
- `GET /api/testgen/generated-tests/` - List generated tests
- `GET /api/testgen/generated-tests/{id}/` - Get test details
- `POST /api/testgen/generated-tests/{id}/regenerate/` - Regenerate test

### Server Configs
- `GET /api/testgen/server-configs/` - List server configs
- `POST /api/testgen/server-configs/` - Create config
- `DELETE /api/testgen/server-configs/{id}/` - Delete config

### CI/CD Pipelines
- `GET /api/testgen/cicd-pipelines/` - List pipelines
- `GET /api/testgen/cicd-pipelines/{id}/` - Get pipeline details

## Configuration

### Environment Variables (Optional)

Create a `.env` file in the project root:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

### Database Configuration

By default, SQLite is used. To use PostgreSQL or MySQL, update `settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'testgen_db',
        'USER': 'your_user',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

## Production Deployment

### Backend Deployment

1. Set `DEBUG = False` in settings.py
2. Configure proper `SECRET_KEY`
3. Set up a production database (PostgreSQL recommended)
4. Collect static files:
```bash
python manage.py collectstatic
```
5. Use gunicorn or uwsgi as WSGI server:
```bash
pip install gunicorn
gunicorn precostcalc.wsgi:application --bind 0.0.0.0:8000
```

### Frontend Deployment

1. Build the React app:
```bash
cd frontend
npm run build
```

2. Serve the `build` directory with nginx or similar:
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        root /path/to/frontend/build;
        try_files $uri /index.html;
    }

    location /api/ {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## Development

### Running Tests

Backend tests:
```bash
python manage.py test
```

Frontend tests:
```bash
cd frontend
npm test
```

### Code Style

Backend:
```bash
pip install black flake8
black .
flake8
```

Frontend:
```bash
cd frontend
npm run lint
```

## Architecture

### Backend Structure
```
testgen/
├── models.py          # Data models (LLMProvider, TestProject, etc.)
├── serializers.py     # DRF serializers
├── views.py           # API viewsets
├── services.py        # Business logic (LLM integration, test generation)
├── urls.py            # API routing
└── admin.py           # Django admin configuration
```

### Frontend Structure
```
frontend/src/
├── components/        # Reusable React components
├── pages/            # Page components (Dashboard, Projects, etc.)
├── services/         # API service layer
├── App.js            # Main app component
└── index.js          # Entry point
```

## Supported LLM Providers

### OpenAI
- Models: GPT-4, GPT-3.5-turbo
- Endpoint: `https://api.openai.com/v1`

### Anthropic
- Models: Claude 3, Claude 2
- Endpoint: `https://api.anthropic.com/v1`

### Google
- Models: Gemini Pro
- Endpoint: `https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent`

### Ollama (Local)
- Any model installed locally
- Endpoint: `http://localhost:11434`
- No API key required

### Custom API
- Configure any OpenAI-compatible API

## License

MIT License - see LICENSE file for details

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## Support

For issues and questions:
- Create an issue on GitHub
- Check existing documentation
- Review API endpoints

## Roadmap

- [ ] Support for more test frameworks (Cypress, TestCafe)
- [ ] Test execution and reporting
- [ ] Integration with test management tools
- [ ] Multi-user collaboration features
- [ ] Docker deployment configuration
- [ ] Kubernetes manifests
- [ ] More CI/CD providers (CircleCI, Jenkins)

## Acknowledgments

Built with Django, React, and powered by modern LLM APIs.
