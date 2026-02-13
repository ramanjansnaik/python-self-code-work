from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    LLMProviderViewSet, TestProjectViewSet, ServerConfigViewSet,
    GeneratedTestViewSet, CICDPipelineViewSet
)

router = DefaultRouter()
router.register(r'llm-providers', LLMProviderViewSet, basename='llmprovider')
router.register(r'projects', TestProjectViewSet, basename='testproject')
router.register(r'server-configs', ServerConfigViewSet, basename='serverconfig')
router.register(r'generated-tests', GeneratedTestViewSet, basename='generatedtest')
router.register(r'cicd-pipelines', CICDPipelineViewSet, basename='cicdpipeline')

urlpatterns = [
    path('', include(router.urls)),
]
