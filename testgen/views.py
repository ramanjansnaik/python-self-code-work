from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import LLMProvider, TestProject, ServerConfig, GeneratedTest, CICDPipeline
from .serializers import (
    LLMProviderSerializer, TestProjectSerializer, TestProjectCreateSerializer,
    ServerConfigSerializer, GeneratedTestSerializer, CICDPipelineSerializer,
    TestGenerationRequestSerializer
)
from .services import TestGeneratorService, CICDGeneratorService


class LLMProviderViewSet(viewsets.ModelViewSet):
    serializer_class = LLMProviderSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return LLMProvider.objects.filter(created_by=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class TestProjectViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return TestProject.objects.filter(created_by=self.request.user)
    
    def get_serializer_class(self):
        if self.action == 'create':
            return TestProjectCreateSerializer
        return TestProjectSerializer
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
    
    @action(detail=True, methods=['post'])
    def generate_tests(self, request, pk=None):
        test_project = self.get_object()
        
        if not test_project.llm_provider:
            return Response(
                {'error': 'LLM provider not configured for this project'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer = TestGenerationRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        config = {
            'include_setup': serializer.validated_data['include_setup'],
            'include_teardown': serializer.validated_data['include_teardown'],
            'headless': serializer.validated_data['headless'],
            'browser': serializer.validated_data['browser'],
            'timeout': serializer.validated_data['timeout'],
        }
        
        generator = TestGeneratorService(test_project)
        generated_tests = []
        errors = []
        
        for scenario in serializer.validated_data['test_scenarios']:
            try:
                test = generator.generate_test(scenario, config)
                generated_tests.append(GeneratedTestSerializer(test).data)
            except Exception as e:
                errors.append({
                    'scenario': scenario,
                    'error': str(e)
                })
        
        return Response({
            'generated_tests': generated_tests,
            'errors': errors,
            'total': len(serializer.validated_data['test_scenarios']),
            'successful': len(generated_tests),
            'failed': len(errors)
        })
    
    @action(detail=True, methods=['post'])
    def generate_cicd(self, request, pk=None):
        test_project = self.get_object()
        
        provider = request.data.get('provider', 'github_actions')
        
        if provider == 'github_actions':
            config_content = CICDGeneratorService.generate_github_actions(test_project)
            file_path = '.github/workflows/tests.yml'
        elif provider == 'gitlab_ci':
            config_content = CICDGeneratorService.generate_gitlab_ci(test_project)
            file_path = '.gitlab-ci.yml'
        else:
            return Response(
                {'error': f'Unsupported CI/CD provider: {provider}'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        cicd_pipeline, created = CICDPipeline.objects.update_or_create(
            test_project=test_project,
            defaults={
                'provider': provider,
                'config_content': config_content,
                'file_path': file_path,
                'on_push': request.data.get('on_push', True),
                'on_pull_request': request.data.get('on_pull_request', True),
                'cron_schedule': request.data.get('cron_schedule', '0 0 * * *'),
            }
        )
        
        return Response({
            'message': 'CI/CD pipeline generated successfully',
            'pipeline': CICDPipelineSerializer(cicd_pipeline).data,
            'created': created
        })
    
    @action(detail=True, methods=['get'])
    def download_tests(self, request, pk=None):
        test_project = self.get_object()
        tests = test_project.generated_tests.filter(status='completed')
        
        return Response({
            'project_name': test_project.name,
            'framework': test_project.framework,
            'language': test_project.language,
            'tests': [
                {
                    'file_name': test.file_name,
                    'test_code': test.test_code,
                    'description': test.test_description,
                }
                for test in tests
            ]
        })


class ServerConfigViewSet(viewsets.ModelViewSet):
    serializer_class = ServerConfigSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        project_id = self.request.query_params.get('project_id')
        queryset = ServerConfig.objects.select_related('test_project')
        
        if project_id:
            queryset = queryset.filter(test_project_id=project_id)
        
        return queryset.filter(test_project__created_by=self.request.user)
    
    def perform_create(self, serializer):
        test_project = get_object_or_404(
            TestProject,
            id=self.request.data.get('test_project'),
            created_by=self.request.user
        )
        serializer.save(test_project=test_project)


class GeneratedTestViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = GeneratedTestSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        project_id = self.request.query_params.get('project_id')
        queryset = GeneratedTest.objects.select_related('test_project')
        
        if project_id:
            queryset = queryset.filter(test_project_id=project_id)
        
        return queryset.filter(test_project__created_by=self.request.user)
    
    @action(detail=True, methods=['post'])
    def regenerate(self, request, pk=None):
        test = self.get_object()
        
        if not test.test_project.llm_provider:
            return Response(
                {'error': 'LLM provider not configured'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        config = {
            'include_setup': True,
            'include_teardown': True,
            'headless': True,
            'browser': 'chromium',
            'timeout': 30000,
        }
        
        generator = TestGeneratorService(test.test_project)
        
        try:
            regenerated_test = generator.generate_test(test.test_description, config)
            return Response(GeneratedTestSerializer(regenerated_test).data)
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class CICDPipelineViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = CICDPipelineSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return CICDPipeline.objects.select_related('test_project').filter(
            test_project__created_by=self.request.user
        )
