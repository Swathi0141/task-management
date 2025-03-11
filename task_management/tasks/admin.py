from django.contrib import admin
from .models import Project, TaskStatus, Task, Comment, Attachment

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('project_name', 'user', 'is_completed')
    search_fields = ('project_name',)
    list_filter = ('is_completed',)

@admin.register(TaskStatus)
class TaskStatusAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('task_title', 'project', 'user', 'status', 'due_date')
    list_filter = ('status', 'due_date')
    search_fields = ('task_title', 'description')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('task', 'user', 'created_at')
    search_fields = ('content',)

@admin.register(Attachment)
class AttachmentAdmin(admin.ModelAdmin):
    list_display = ('file_name', 'task', 'user', 'file_type', 'uploaded_at')
    search_fields = ('file_name',)