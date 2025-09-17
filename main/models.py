from django.db import models

# Create your models here.
import uuid
from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.IntegerField()
    description = models.TextField()
    stock = models.IntegerField(default=0)
    color = models.CharField(max_length=50, blank=True)
    size = models.CharField(max_length=50, blank=True)

    thumbnail = models.URLField(blank=True, null=True)
    category = models.CharField(max_length=100)
    is_featured = models.BooleanField(default=False)
    views = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return self.name
    
    def increment_views(self):
        self.views += 1
        self.save(update_fields=['views'])
    