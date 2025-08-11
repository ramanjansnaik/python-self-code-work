from django.urls import path
from . import views, api_views

urlpatterns = [
    path('', views.index, name='index'),
    path('api/block-types/', api_views.get_block_types),
    path('api/save-project/', api_views.save_project),
]
