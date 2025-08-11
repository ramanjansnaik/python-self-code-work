from django.db import models
from django.contrib.auth.models import User

class BlockType(models.Model):
    name = models.CharField(max_length=100)
    price_per_sqft = models.DecimalField(max_digits=10, decimal_places=2)

class Project(models.Model):
    name = models.CharField(max_length=200)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class BlockInstance(models.Model):
    project = models.ForeignKey(Project, related_name='blocks', on_delete=models.CASCADE)
    block_type = models.ForeignKey(BlockType, on_delete=models.CASCADE)
    length = models.FloatField()
    width = models.FloatField()
    x = models.FloatField(default=0)
    y = models.FloatField(default=0)
