from django.urls import path
from . import views

urlpatterns = [
    path('', views.default_video_page, name='default_video_page'),
    path('<slug:slug>/', views.video_page, name='video_page'),
    path('increment-view/<slug:slug>/', views.increment_view, name='increment_view'),

    path('<slug:slug>/comment/', views.post_comment, name='post_comment'),
    path('<slug:slug>/comment/<int:comment_id>/reply/', views.post_reply, name='post_reply'),
    path('<slug:slug>/comment/<int:comment_id>/delete/', views.delete_comment, name='delete_comment'),
]