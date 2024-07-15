from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Video

@login_required
def video_page(request, video_id):
    video = get_object_or_404(Video, id=video_id)
    next_video = Video.objects.filter(id__gt=video_id).order_by('id').first()
    previous_video = Video.objects.filter(id__lt=video_id).order_by('-id').first()

    context = {
        'video': video,
        'next_video': next_video,
        'previous_video': previous_video,
    }
    return render(request, 'videos/video_page.html', context)