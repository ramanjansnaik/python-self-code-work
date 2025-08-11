from django.contrib import admin
from .models import BlockType, Project, BlockInstance

admin.site.register(BlockType)
admin.site.register(Project)
admin.site.register(BlockInstance)
