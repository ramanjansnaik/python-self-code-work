# Quick Start Guide

Get TestGen up and running in 5 minutes!

## Installation

### Option 1: Automated Installation (Recommended)

```bash
./install.sh
```

This script will:
- Create a Python virtual environment
- Install all backend dependencies
- Run database migrations
- Create a superuser
- Install frontend dependencies (if Node.js is available)

### Option 2: Manual Installation

#### Backend

```bash
# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser
```

#### Frontend

```bash
cd frontend
npm install
```

## Running the Application

### Start Backend

```bash
# Activate virtual environment
source .venv/bin/activate

# Start Django server
python manage.py runserver
```

Backend will be available at: `http://localhost:8000`

### Start Frontend

Open a new terminal:

```bash
cd frontend
npm start
```

Frontend will be available at: `http://localhost:3000`

## First Steps

### 1. Configure an LLM Provider

1. Go to `http://localhost:3000`
2. Click on **LLM Providers** in the navigation
3. Click **+ Add Provider**
4. Fill in the details:

**For OpenAI:**
- Name: `My OpenAI`
- Provider Type: `OpenAI`
- API Endpoint: `https://api.openai.com/v1`
- API Key: Your OpenAI API key
- Model Name: `gpt-4` or `gpt-3.5-turbo`

**For Local Ollama:**
- Name: `Local Ollama`
- Provider Type: `Ollama (Local)`
- API Endpoint: `http://localhost:11434`
- Model Name: `llama2` (or any installed model)
- API Key: Leave empty

### 2. Create a Test Project

1. Click **Projects** → **+ Create Project**
2. Fill in:
   - Project Name: `My E-commerce Tests`
   - Description: `Automated tests for my online store`
   - Website URL: `https://example.com`
   - Framework: `Playwright`
   - Language: `Python`
   - LLM Provider: Select the provider you created
3. (Optional) Add server configurations
4. Click **Create Project**

### 3. Generate Tests

1. Open your project
2. In the **Generate Tests** section, add test scenarios:
   - `Test user login with valid credentials`
   - `Test adding items to shopping cart`
   - `Test checkout process with payment`
3. Configure test options (browser, timeout, etc.)
4. Click **🤖 Generate Tests**
5. Wait for AI to generate your tests
6. Download the generated test files

### 4. Generate CI/CD Pipeline

1. Scroll to **CI/CD Pipeline Configuration**
2. Select provider: `GitHub Actions` or `GitLab CI`
3. Configure triggers and schedule
4. Click **⚙️ Generate Pipeline**
5. Download the pipeline configuration file
6. Add it to your repository:
   - GitHub Actions: `.github/workflows/tests.yml`
   - GitLab CI: `.gitlab-ci.yml`

## Example API Usage

You can also use the REST API directly:

### Create LLM Provider

```bash
curl -X POST http://localhost:8000/api/testgen/llm-providers/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "My OpenAI",
    "provider_type": "openai",
    "api_endpoint": "https://api.openai.com/v1",
    "api_key": "sk-...",
    "model_name": "gpt-4"
  }'
```

### Create Project

```bash
curl -X POST http://localhost:8000/api/testgen/projects/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test Project",
    "website_url": "https://example.com",
    "framework": "playwright",
    "language": "python",
    "llm_provider": 1
  }'
```

### Generate Tests

```bash
curl -X POST http://localhost:8000/api/testgen/projects/1/generate_tests/ \
  -H "Content-Type: application/json" \
  -d '{
    "test_scenarios": [
      "Test user login",
      "Test product search"
    ],
    "headless": true,
    "browser": "chromium"
  }'
```

## Troubleshooting

### Backend Issues

**Migration errors:**
```bash
python manage.py makemigrations
python manage.py migrate
```

**Port already in use:**
```bash
python manage.py runserver 8001
```

### Frontend Issues

**Port already in use:**
Edit `frontend/package.json` and change the port:
```json
"scripts": {
  "start": "PORT=3001 react-scripts start"
}
```

**Cannot connect to backend:**
- Ensure Django is running on `http://localhost:8000`
- Check CORS settings in `precostcalc/settings.py`

### LLM Provider Issues

**OpenAI API errors:**
- Verify your API key is correct
- Check you have sufficient credits
- Ensure the model name is correct (`gpt-4`, `gpt-3.5-turbo`)

**Ollama connection errors:**
- Ensure Ollama is running: `ollama serve`
- Verify the endpoint: `http://localhost:11434`
- Check you have a model installed: `ollama list`

## Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Explore the Django admin interface at `http://localhost:8000/admin`
- Check out the API documentation
- Configure multiple environments with server configs
- Set up your CI/CD pipeline in your repository

## Support

For issues and questions:
- Check the [README.md](README.md)
- Review the troubleshooting section above
- Create an issue on GitHub

Happy testing! 🚀
