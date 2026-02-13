from rest_framework import serializers
from .models import LLMProvider, TestProject, ServerConfig, GeneratedTest, CICDPipeline


class LLMProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = LLMProvider
        fields = ['id', 'name', 'provider_type', 'api_endpoint', 'api_key', 'model_name', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
        extra_kwargs = {
            'api_key': {'write_only': True}
        }


class ServerConfigSerializer(serializers.ModelSerializer):
    base_url = serializers.ReadOnlyField()
    
    class Meta:
        model = ServerConfig
        fields = ['id', 'hostname', 'port', 'protocol', 'username', 'ssh_key', 'environment_vars', 'base_url', 'created_at']
        read_only_fields = ['id', 'created_at']
        extra_kwargs = {
            'ssh_key': {'write_only': True}
        }


class GeneratedTestSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeneratedTest
        fields = ['id', 'test_name', 'test_description', 'test_code', 'file_name', 'status', 
                  'error_message', 'llm_prompt', 'llm_response', 'generation_time', 'created_at', 'updated_at']
        read_only_fields = ['id', 'status', 'error_message', 'generation_time', 'created_at', 'updated_at']


class CICDPipelineSerializer(serializers.ModelSerializer):
    class Meta:
        model = CICDPipeline
        fields = ['id', 'provider', 'config_content', 'file_path', 'cron_schedule', 
                  'on_push', 'on_pull_request', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class TestProjectSerializer(serializers.ModelSerializer):
    server_configs = ServerConfigSerializer(many=True, read_only=True)
    generated_tests = GeneratedTestSerializer(many=True, read_only=True)
    cicd_pipeline = CICDPipelineSerializer(read_only=True)
    llm_provider_details = LLMProviderSerializer(source='llm_provider', read_only=True)
    
    class Meta:
        model = TestProject
        fields = ['id', 'name', 'description', 'website_url', 'framework', 'language', 
                  'llm_provider', 'llm_provider_details', 'server_configs', 'generated_tests', 
                  'cicd_pipeline', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class TestProjectCreateSerializer(serializers.ModelSerializer):
    server_configs = ServerConfigSerializer(many=True, required=False)
    
    class Meta:
        model = TestProject
        fields = ['id', 'name', 'description', 'website_url', 'framework', 'language', 
                  'llm_provider', 'server_configs', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def create(self, validated_data):
        server_configs_data = validated_data.pop('server_configs', [])
        test_project = TestProject.objects.create(**validated_data)
        
        for server_config_data in server_configs_data:
            ServerConfig.objects.create(test_project=test_project, **server_config_data)
        
        return test_project


class TestGenerationRequestSerializer(serializers.Serializer):
    test_scenarios = serializers.ListField(
        child=serializers.CharField(max_length=500),
        required=True,
        help_text="List of test scenarios to generate"
    )
    include_setup = serializers.BooleanField(default=True)
    include_teardown = serializers.BooleanField(default=True)
    headless = serializers.BooleanField(default=True)
    browser = serializers.ChoiceField(
        choices=['chromium', 'firefox', 'webkit'],
        default='chromium'
    )
    timeout = serializers.IntegerField(default=30000, min_value=1000, max_value=120000)
