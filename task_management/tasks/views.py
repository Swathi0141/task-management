from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Project, Task, Comment, Attachment
from .forms import ProjectForm, TaskForm, CommentForm  
from django.http import JsonResponse
from .serializers import ProjectSerializer, TaskSerializer, AttachmentSerializer, CommentSerializer
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

@api_view(['GET', 'POST'])
@login_required
def comment_list(request, format=None):
    if request.method == 'GET':
        comments = Comment.objects.filter(user=request.user)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@login_required
def comment_detail(request, pk, format=None):
    comment = get_object_or_404(Comment, pk=pk, user=request.user)

    if request.method == 'GET':
        serializer = CommentSerializer(comment)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = CommentSerializer(comment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST'])
@login_required
def attachment_list(request, format=None):
    if request.method == 'GET':
        attachments = Attachment.objects.filter(user=request.user)
        serializer = AttachmentSerializer(attachments, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        serializer = AttachmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@login_required
def attachment_detail(request, pk, format=None):
    attachment = get_object_or_404(Attachment, pk=pk, user=request.user)

    if request.method == 'GET':
        serializer = AttachmentSerializer(attachment)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = AttachmentSerializer(attachment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        attachment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)