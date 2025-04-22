from django.urls import path
from django.views.generic import RedirectView
from . import views
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework_simplejwt.views import (TokenRefreshView, TokenBlacklistView)
from .views import GoogleLoginView, employee_list, employee_detail

urlpatterns = [
    path('', RedirectView.as_view(pattern_name='task_list'), name='index'),
    path('projects/', views.project_list, name='project_list'),
    path('projects/<int:pk>/', views.project_detail, name='project_detail'),
    path('tasks/', views.task_list, name='task_list'),
    path('tasks/<int:pk>/', views.task_detail, name='task_detail'),
    path('comments/', views.comment_list, name='comment_list'),
    path('comments/<int:pk>/', views.comment_detail, name='comment_detail'),
    path('attachments/', views.attachment_list, name='attachment_list'),
    path('attachments/<int:pk>/', views.attachment_detail, name='attachment_detail'),
    path('employees/', employee_list, name='employee_list'),
    path('employees/<int:pk>/', employee_detail, name='employee_detail'),
    
    path('api/v1/token/google/', GoogleLoginView.as_view(), name="google-login"),
    path('api/v1/token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('api/v1/token/logout/', TokenBlacklistView.as_view(), name='token-blacklist'),
]

urlpatterns = format_suffix_patterns(urlpatterns)