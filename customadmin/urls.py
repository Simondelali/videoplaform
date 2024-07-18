from django.urls import path
from . import views

app_name = 'customadmin'

urlpatterns = [
    path('', views.video_list, name='video_list'),
    path('upload/', views.video_upload, name='video_upload'),
    path('edit/<int:video_id>/', views.video_edit, name='video_edit'),
    path('delete/<int:video_id>/', views.video_delete, name='video_delete'),
]