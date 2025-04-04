from django.urls import path
from django.views.generic import RedirectView
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

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
]

urlpatterns = format_suffix_patterns(urlpatterns)