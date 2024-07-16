from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Video

@login_required
def video_page(request):
    videos = list(Video.objects.all().order_by('id'))
    total_videos = len(videos)
    
    current_index = int(request.GET.get('index', 0))
    
    if current_index < 0:
        current_index = 0
    elif current_index >= total_videos:
        current_index = total_videos - 1
    
    current_video = videos[current_index] if videos else None
    
    context = {
        'video': current_video,
        'has_previous': current_index > 0,
        'has_next': current_index < total_videos - 1,
        'previous_index': current_index - 1,
        'next_index': current_index + 1,
        'current_index': current_index,
        'total_videos': total_videos,
    }
    return render(request, 'videos/video_page.html', context)