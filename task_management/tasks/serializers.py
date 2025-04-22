from rest_framework import serializers
from .models import Project, Task, TaskStatus, Comment, Attachment
from django.contrib.auth.models import User
from google.auth.transport import requests
from google.oauth2 import id_token
from rest_framework_simplejwt.tokens import RefreshToken

class GoogleAuthSerializer(serializers.Serializer):
    token = serializers.CharField()

    def validate(self, attrs):
        token = attrs.get("token")
        try:
            idinfo = id_token.verify_oauth2_token(token, requests.Request())

            email = idinfo.get("email")
            name = idinfo.get("name")

            if not email:
                raise serializers.ValidationError("Email not available")

            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                raise serializers.ValidationError("You are not authorized to log in.")

            refresh = RefreshToken.for_user(user)
            return {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "user": {
                    "email": user.email,
                    "name": user.first_name,
                },
            }
        except ValueError:
            raise serializers.ValidationError("Invalid token")

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

class EmployeeSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'full_name', 'email']

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"