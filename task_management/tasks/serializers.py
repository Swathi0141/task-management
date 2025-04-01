from rest_framework import serializers
from .models import Project, Task, TaskStatus, Comment, Attachment

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'project_name', 'is_completed']

class TaskSerializer(serializers.ModelSerializer):
    status = serializers.SlugRelatedField(
        queryset=TaskStatus.objects.all(),
        slug_field='name'
    )   
    class Meta:
        model = Task
        fields = ['id', 'task_title', 'description', 'project', 'status', 'due_date']
        
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['content']
        

class AttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attachment
        fields = ['file']