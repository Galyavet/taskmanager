from django.db import models


class Task(models.Model):
    name = models.CharField(max_length=255)
    owner_email = models.EmailField(max_length=255, default=None)
    description = models.TextField(null=True, blank=True)
    complexity = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created_at']
