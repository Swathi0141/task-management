from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Project, Task
from .forms import ProjectForm, TaskForm, CommentForm  
from django.http import JsonResponse
from .serializers import ProjectSerializer, TaskSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
 
@api_view(['GET', 'POST'])
@login_required
def project_list(request, format=None):
    
    if request.method == 'GET':
        projects = Project.objects.filter(user=request.user)
        serializer = ProjectSerializer(projects, many = True)
        return Response({'projects': serializer.data})

    if request.method == 'POST':
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET', 'PUT', 'DELETE'])         
@login_required
def project_detail(request, pk, format=None):
    
    project = get_object_or_404(Project, pk=pk, user=request.user)
    tasks = Task.objects.filter(project=project)
    # return render(request, 'tasks/project_detail.html', {'project': project, 'tasks': tasks})

    if request.method == 'GET':
        serializer = ProjectSerializer(project)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        projectserializer = ProjectSerializer(project, data=request.data)
        if projectserializer.is_valid():
            projectserializer.save()
            return Response(projectserializer.data)
        return Response(projectserializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        project.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST'])
@login_required
def task_list(request, format=None):
    
    if request.method == 'GET':
        tasks = Task.objects.filter(user=request.user)
        task_serializer = TaskSerializer(tasks, many=True)
        return Response(task_serializer.data)

    if request.method == 'POST':
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])        
@login_required
def task_detail(request, pk, format=None):
    
    task = get_object_or_404(Task, pk=pk, user=request.user)
    comments = task.comments.all().order_by('-created_at')
    attachments = task.attachments.all()
    
    if request.method == 'GET':
        serializer = TaskSerializer(task)
        return Response(serializer.data)
    
    # elif request.method == 'POST':
    #     form = CommentForm(request.POST)
    #     if form.is_valid():
    #         comment = form.save(commit=False)
    #         comment.task = task
    #         comment.user = request.user
    #         comment.save()
    #         return redirect('task_detail')
    
    elif request.method == 'PUT':
        tskserializer = TaskSerializer(task, data=request.data)
        if tskserializer.is_valid():
            tskserializer.save()
            return Response(tskserializer.data)
        return Response(tskserializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    else:
        form = CommentForm()
        
    return render(request, 'tasks/task_detail.html', {
        'task': task, 
        'comments': comments,
        'attachments': attachments,
        'form': form
    })