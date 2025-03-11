from django import forms
from .models import Project, Task, Comment, Attachment

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['project_name', 'is_completed']

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['task_title', 'description', 'project', 'status', 'due_date']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'})
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3})
        }

class AttachmentForm(forms.ModelForm):
    class Meta:
        model = Attachment
        fields = ['file']