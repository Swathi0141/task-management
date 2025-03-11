from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Project, Task, TaskStatus
from .forms import ProjectForm, TaskForm, CommentForm  # We'll create these forms

@login_required
def project_list(request):
    projects = Project.objects.filter(user=request.user)
    return render(request, 'tasks/project_list.html', {'projects': projects})

@login_required
def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk, user=request.user)
    tasks = Task.objects.filter(project=project)
    return render(request, 'tasks/project_detail.html', {'project': project, 'tasks': tasks})

@login_required
def task_list(request):
    tasks = Task.objects.filter(user=request.user)
    return render(request, 'tasks/task_list.html', {'tasks': tasks})

@login_required
def task_detail(request, pk):
    task = get_object_or_404(Task, pk=pk)
    comments = task.comments.all().order_by('-created_at')
    attachments = task.attachments.all()
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.task = task
            comment.user = request.user
            comment.save()
            return redirect('task_detail', pk=task.pk)
    else:
        form = CommentForm()
        
    return render(request, 'tasks/task_detail.html', {
        'task': task, 
        'comments': comments,
        'attachments': attachments,
        'form': form
    })