from django.conf import settings
from django.db import models

class BaseModel(models.Model):

    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, auto_created=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='+', null=True, blank=True, on_delete=models.SET_NULL)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='+', null=True, blank=True, on_delete=models.SET_NULL)

    class Meta:
        abstract = True

class Todo(BaseModel):
    """
    Todo model to store task information
    """
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    completed = models.BooleanField(default=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='todos', on_delete=models.CASCADE)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title
