from django.db import models

class CareerPath(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    requirements = models.TextField()
    average_salary = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class CareerTool(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    tool_type = models.CharField(max_length=50)  # e.g., 'template', 'calculator', 'guide'
    file_url = models.URLField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title