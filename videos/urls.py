from django.urls import path
from . import views

urlpatterns = [
    path('video/<int:video_id>/', views.video_page, name='video_page'),
]