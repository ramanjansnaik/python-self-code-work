from django.db import models
from django.contrib.auth.models import User

class LLMProvider(models.Model):
    PROVIDER_CHOICES = [
        ('openai', 'OpenAI'),
        ('anthropic', 'Anthropic'),
        ('google', 'Google'),
        ('ollama', 'Ollama (Local)'),
        ('custom', 'Custom API'),
    ]
    
    name = models.CharField(max_length=100)
    provider_type = models.CharField(max_length=20, choices=PROVIDER_CHOICES, default='openai')
    api_endpoint = models.URLField(max_length=500)
    api_key = models.CharField(max_length=500, blank=True, null=True)
    model_name = models.CharField(max_length=100, default='gpt-4')
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='llm_providers')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} ({self.provider_type})"


class TestProject(models.Model):
    FRAMEWORK_CHOICES = [
        ('playwright', 'Playwright'),
        ('selenium', 'Selenium'),
    ]
    
    LANGUAGE_CHOICES = [
        ('python', 'Python'),
        ('javascript', 'JavaScript'),
        ('typescript', 'TypeScript'),
        ('java', 'Java'),
        ('csharp', 'C#'),
    ]
    
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    website_url = models.URLField(max_length=500)
    framework = models.CharField(max_length=20, choices=FRAMEWORK_CHOICES, default='playwright')
    language = models.CharField(max_length=20, choices=LANGUAGE_CHOICES, default='python')
    llm_provider = models.ForeignKey(LLMProvider, on_delete=models.SET_NULL, null=True, related_name='test_projects')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='test_projects')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name


class ServerConfig(models.Model):
    test_project = models.ForeignKey(TestProject, on_delete=models.CASCADE, related_name='server_configs')
    hostname = models.CharField(max_length=255)
    port = models.IntegerField(default=80)
    protocol = models.CharField(max_length=10, choices=[('http', 'HTTP'), ('https', 'HTTPS')], default='https')
    username = models.CharField(max_length=100, blank=True, null=True)
    ssh_key = models.TextField(blank=True, null=True)
    environment_vars = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['test_project', 'hostname']
    
    def __str__(self):
        return f"{self.hostname}:{self.port} ({self.test_project.name})"
    
    @property
    def base_url(self):
        return f"{self.protocol}://{self.hostname}:{self.port}"


class GeneratedTest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('generating', 'Generating'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]
    
    test_project = models.ForeignKey(TestProject, on_delete=models.CASCADE, related_name='generated_tests')
    test_name = models.CharField(max_length=200)
    test_description = models.TextField(blank=True)
    test_code = models.TextField()
    file_name = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    error_message = models.TextField(blank=True, null=True)
    llm_prompt = models.TextField(blank=True)
    llm_response = models.TextField(blank=True)
    generation_time = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.test_name} ({self.test_project.name})"


class CICDPipeline(models.Model):
    PROVIDER_CHOICES = [
        ('github_actions', 'GitHub Actions'),
        ('gitlab_ci', 'GitLab CI'),
        ('jenkins', 'Jenkins'),
        ('circleci', 'CircleCI'),
    ]
    
    test_project = models.OneToOneField(TestProject, on_delete=models.CASCADE, related_name='cicd_pipeline')
    provider = models.CharField(max_length=20, choices=PROVIDER_CHOICES, default='github_actions')
    config_content = models.TextField()
    file_path = models.CharField(max_length=255)
    cron_schedule = models.CharField(max_length=100, blank=True, null=True)
    on_push = models.BooleanField(default=True)
    on_pull_request = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.provider} - {self.test_project.name}"
