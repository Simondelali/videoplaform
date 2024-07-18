from django.urls import path
from . import views

urlpatterns = [
    path('', views.default_video_page, name='default_video_page'),
    path('<slug:slug>/', views.video_page, name='video_page'),
    path('increment-view/<slug:slug>/', views.increment_view, name='increment_view'),
]