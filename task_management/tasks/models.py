from django.db import models
from django.contrib.auth.models import User  # We'll use Django's built-in User model

class Project(models.Model):
    project_name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='projects')
    is_completed = models.BooleanField(default=False)
    
    def __str__(self):
        return self.project_name

class TaskStatus(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200, blank=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Task Statuses"

class Task(models.Model):
    task_title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assigned_tasks')
    status = models.ForeignKey(TaskStatus, on_delete=models.CASCADE, related_name='tasks')
    due_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.task_title

class Comment(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Comment by {self.user.username} on {self.task.task_title}"

class Attachment(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='attachments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='uploads')
    file_name = models.CharField(max_length=100)
    file_type = models.CharField(max_length=50)
    file = models.FileField(upload_to='attachments/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.file_name