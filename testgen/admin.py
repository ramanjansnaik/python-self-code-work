from django.contrib import admin
from .models import LLMProvider, TestProject, ServerConfig, GeneratedTest, CICDPipeline


@admin.register(LLMProvider)
class LLMProviderAdmin(admin.ModelAdmin):
    list_display = ['name', 'provider_type', 'model_name', 'is_active', 'created_by', 'created_at']
    list_filter = ['provider_type', 'is_active', 'created_at']
    search_fields = ['name', 'model_name']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(TestProject)
class TestProjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'framework', 'language', 'website_url', 'created_by', 'created_at']
    list_filter = ['framework', 'language', 'created_at']
    search_fields = ['name', 'website_url', 'description']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(ServerConfig)
class ServerConfigAdmin(admin.ModelAdmin):
    list_display = ['test_project', 'hostname', 'port', 'protocol', 'created_at']
    list_filter = ['protocol', 'created_at']
    search_fields = ['hostname', 'test_project__name']
    readonly_fields = ['created_at']


@admin.register(GeneratedTest)
class GeneratedTestAdmin(admin.ModelAdmin):
    list_display = ['test_name', 'test_project', 'status', 'generation_time', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['test_name', 'test_project__name', 'test_description']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(CICDPipeline)
class CICDPipelineAdmin(admin.ModelAdmin):
    list_display = ['test_project', 'provider', 'on_push', 'on_pull_request', 'created_at']
    list_filter = ['provider', 'on_push', 'on_pull_request', 'created_at']
    search_fields = ['test_project__name']
    readonly_fields = ['created_at', 'updated_at']
