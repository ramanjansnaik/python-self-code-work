import time
import json
from typing import Dict, List, Optional

try:
    import requests
except ImportError:  # pragma: no cover - handled for environments without optional deps
    requests = None

from .models import LLMProvider, TestProject, GeneratedTest


class LLMService:
    def __init__(self, provider: LLMProvider):
        self.provider = provider
    
    def generate_completion(self, prompt: str, max_tokens: int = 2000) -> Dict:
        if requests is None:
            raise ImportError('The requests library is required for LLM provider calls.')

        if self.provider.provider_type == 'openai':
            return self._openai_completion(prompt, max_tokens)
        elif self.provider.provider_type == 'anthropic':
            return self._anthropic_completion(prompt, max_tokens)
        elif self.provider.provider_type == 'google':
            return self._google_completion(prompt, max_tokens)
        elif self.provider.provider_type == 'ollama':
            return self._ollama_completion(prompt, max_tokens)
        elif self.provider.provider_type == 'custom':
            return self._custom_api_completion(prompt, max_tokens)
        else:
            raise ValueError(f"Unsupported provider type: {self.provider.provider_type}")
    
    def _openai_completion(self, prompt: str, max_tokens: int) -> Dict:
        headers = {
            'Authorization': f'Bearer {self.provider.api_key}',
            'Content-Type': 'application/json',
        }
        
        payload = {
            'model': self.provider.model_name,
            'messages': [
                {'role': 'system', 'content': 'You are an expert test automation engineer. Generate clean, executable test code.'},
                {'role': 'user', 'content': prompt}
            ],
            'max_tokens': max_tokens,
            'temperature': 0.7,
        }
        
        response = requests.post(
            f"{self.provider.api_endpoint}/chat/completions",
            headers=headers,
            json=payload,
            timeout=120
        )
        response.raise_for_status()
        
        result = response.json()
        return {
            'content': result['choices'][0]['message']['content'],
            'model': result['model'],
            'usage': result.get('usage', {})
        }
    
    def _anthropic_completion(self, prompt: str, max_tokens: int) -> Dict:
        headers = {
            'x-api-key': self.provider.api_key,
            'anthropic-version': '2023-06-01',
            'Content-Type': 'application/json',
        }
        
        payload = {
            'model': self.provider.model_name,
            'max_tokens': max_tokens,
            'messages': [
                {'role': 'user', 'content': prompt}
            ],
        }
        
        response = requests.post(
            f"{self.provider.api_endpoint}/messages",
            headers=headers,
            json=payload,
            timeout=120
        )
        response.raise_for_status()
        
        result = response.json()
        return {
            'content': result['content'][0]['text'],
            'model': result['model'],
            'usage': result.get('usage', {})
        }
    
    def _google_completion(self, prompt: str, max_tokens: int) -> Dict:
        headers = {
            'Content-Type': 'application/json',
        }
        
        url = f"{self.provider.api_endpoint}?key={self.provider.api_key}"
        
        payload = {
            'contents': [
                {'parts': [{'text': prompt}]}
            ],
            'generationConfig': {
                'maxOutputTokens': max_tokens,
                'temperature': 0.7,
            }
        }
        
        response = requests.post(url, headers=headers, json=payload, timeout=120)
        response.raise_for_status()
        
        result = response.json()
        return {
            'content': result['candidates'][0]['content']['parts'][0]['text'],
            'model': self.provider.model_name,
            'usage': result.get('usageMetadata', {})
        }
    
    def _ollama_completion(self, prompt: str, max_tokens: int) -> Dict:
        payload = {
            'model': self.provider.model_name,
            'prompt': prompt,
            'stream': False,
            'options': {
                'num_predict': max_tokens,
            }
        }
        
        response = requests.post(
            f"{self.provider.api_endpoint}/api/generate",
            json=payload,
            timeout=120
        )
        response.raise_for_status()
        
        result = response.json()
        return {
            'content': result['response'],
            'model': result['model'],
            'usage': {}
        }
    
    def _custom_api_completion(self, prompt: str, max_tokens: int) -> Dict:
        headers = {
            'Content-Type': 'application/json',
        }
        
        if self.provider.api_key:
            headers['Authorization'] = f'Bearer {self.provider.api_key}'
        
        payload = {
            'prompt': prompt,
            'max_tokens': max_tokens,
        }
        
        response = requests.post(
            self.provider.api_endpoint,
            headers=headers,
            json=payload,
            timeout=120
        )
        response.raise_for_status()
        
        result = response.json()
        return {
            'content': result.get('content', result.get('text', result.get('response', ''))),
            'model': self.provider.model_name,
            'usage': result.get('usage', {})
        }


class TestGeneratorService:
    def __init__(self, test_project: TestProject):
        self.test_project = test_project
        self.llm_service = LLMService(test_project.llm_provider)
    
    def generate_test(self, scenario: str, config: Dict) -> GeneratedTest:
        start_time = time.time()
        
        test = GeneratedTest.objects.create(
            test_project=self.test_project,
            test_name=self._generate_test_name(scenario),
            test_description=scenario,
            test_code='',
            file_name=self._generate_file_name(scenario),
            status='generating',
        )
        
        try:
            prompt = self._build_prompt(scenario, config)
            test.llm_prompt = prompt
            test.save()
            
            response = self.llm_service.generate_completion(prompt)
            
            test.llm_response = json.dumps(response)
            test.test_code = self._extract_code_from_response(response['content'])
            test.status = 'completed'
            test.generation_time = time.time() - start_time
            test.save()
            
            return test
            
        except Exception as e:
            test.status = 'failed'
            test.error_message = str(e)
            test.generation_time = time.time() - start_time
            test.save()
            raise
    
    def _build_prompt(self, scenario: str, config: Dict) -> str:
        framework = self.test_project.framework
        language = self.test_project.language
        website_url = self.test_project.website_url
        
        server_configs = self.test_project.server_configs.all()
        server_info = ""
        if server_configs.exists():
            server_config = server_configs.first()
            server_info = f"\nBase URL: {server_config.base_url}"
        
        prompt_template = f"""Generate a complete, executable {framework} test in {language} for the following scenario:

Website: {website_url}{server_info}
Scenario: {scenario}

Requirements:
- Framework: {framework}
- Language: {language}
- Browser: {config.get('browser', 'chromium')}
- Headless mode: {config.get('headless', True)}
- Default timeout: {config.get('timeout', 30000)}ms
- Include setup: {config.get('include_setup', True)}
- Include teardown: {config.get('include_teardown', True)}

Generate only the test code with proper imports, setup, test logic, and teardown.
Include comments for clarity.
Make sure the test is production-ready and follows best practices.
Return ONLY the code, no explanations before or after.
"""
        
        return prompt_template
    
    def _extract_code_from_response(self, response_content: str) -> str:
        lines = response_content.strip().split('\n')
        
        code_start = None
        code_end = None
        
        for i, line in enumerate(lines):
            if line.strip().startswith('```'):
                if code_start is None:
                    code_start = i + 1
                else:
                    code_end = i
                    break
        
        if code_start is not None and code_end is not None:
            return '\n'.join(lines[code_start:code_end])
        
        return response_content.strip()
    
    def _generate_test_name(self, scenario: str) -> str:
        name = scenario.lower()
        name = ''.join(c if c.isalnum() or c.isspace() else ' ' for c in name)
        name = '_'.join(name.split())
        return f"test_{name[:50]}"
    
    def _generate_file_name(self, scenario: str) -> str:
        name = self._generate_test_name(scenario)
        
        extensions = {
            'python': '.py',
            'javascript': '.js',
            'typescript': '.ts',
            'java': '.java',
            'csharp': '.cs',
        }
        
        ext = extensions.get(self.test_project.language, '.py')
        return f"{name}{ext}"


class CICDGeneratorService:
    @staticmethod
    def generate_github_actions(test_project: TestProject) -> str:
        framework = test_project.framework
        language = test_project.language
        
        config = {
            'playwright-python': """name: Playwright Tests

on:
  push:
    branches: [ main, master ]
  pull_request:
    branches: [ main, master ]
  schedule:
    - cron: '0 0 * * *'

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python
      uses: actions/setup-python@v5
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install playwright pytest-playwright
        playwright install
    
    - name: Run tests
      run: |
        pytest tests/ --html=report.html --self-contained-html
    
    - name: Upload test results
      if: always()
      uses: actions/upload-artifact@v4
      with:
        name: test-results
        path: report.html
""",
            'playwright-javascript': """name: Playwright Tests

on:
  push:
    branches: [ main, master ]
  pull_request:
    branches: [ main, master ]
  schedule:
    - cron: '0 0 * * *'

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Node.js
      uses: actions/setup-node@v4
      with:
        node-version: '20'
    
    - name: Install dependencies
      run: |
        npm install
        npx playwright install
    
    - name: Run tests
      run: |
        npm test
    
    - name: Upload test results
      if: always()
      uses: actions/upload-artifact@v4
      with:
        name: test-results
        path: playwright-report/
""",
            'playwright-typescript': """name: Playwright Tests

on:
  push:
    branches: [ main, master ]
  pull_request:
    branches: [ main, master ]
  schedule:
    - cron: '0 0 * * *'

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Node.js
      uses: actions/setup-node@v4
      with:
        node-version: '20'
    
    - name: Install dependencies
      run: |
        npm install
        npx playwright install
    
    - name: Run tests
      run: |
        npm test
    
    - name: Upload test results
      if: always()
      uses: actions/upload-artifact@v4
      with:
        name: test-results
        path: playwright-report/
""",
            'selenium-python': """name: Selenium Tests

on:
  push:
    branches: [ main, master ]
  pull_request:
    branches: [ main, master ]
  schedule:
    - cron: '0 0 * * *'

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python
      uses: actions/setup-python@v5
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install selenium pytest webdriver-manager
    
    - name: Run tests
      run: |
        pytest tests/ --html=report.html --self-contained-html
    
    - name: Upload test results
      if: always()
      uses: actions/upload-artifact@v4
      with:
        name: test-results
        path: report.html
""",
            'selenium-java': """name: Selenium Tests

on:
  push:
    branches: [ main, master ]
  pull_request:
    branches: [ main, master ]
  schedule:
    - cron: '0 0 * * *'

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up JDK
      uses: actions/setup-java@v4
      with:
        java-version: '17'
        distribution: 'temurin'
    
    - name: Run tests with Maven
      run: mvn test
    
    - name: Upload test results
      if: always()
      uses: actions/upload-artifact@v4
      with:
        name: test-results
        path: target/surefire-reports/
""",
        }
        
        key = f"{framework}-{language}"
        return config.get(key, config.get(f"{framework}-python", config['playwright-python']))
    
    @staticmethod
    def generate_gitlab_ci(test_project: TestProject) -> str:
        framework = test_project.framework
        language = test_project.language
        
        if framework == 'playwright' and language == 'python':
            return """image: python:3.11

stages:
  - test

test:
  stage: test
  before_script:
    - pip install playwright pytest-playwright
    - playwright install
  script:
    - pytest tests/ --html=report.html --self-contained-html
  artifacts:
    when: always
    paths:
      - report.html
    expire_in: 30 days
"""
        
        return """stages:
  - test

test:
  stage: test
  script:
    - echo "Configure your test command here"
  artifacts:
    when: always
    paths:
      - test-results/
"""
