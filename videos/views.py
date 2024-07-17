from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Video

@login_required
def default_video_page(request):
    first_video = Video.objects.order_by('id').first()
    if first_video:
        return redirect('video_page', slug=first_video.slug)
    else:
        return render(request, 'videos/no_videos.html')

@login_required
def video_page(request, slug):
    video = get_object_or_404(Video, slug=slug)
    videos = Video.objects.exclude(id=video.id).order_by('?')[:5]

    all_videos = list(Video.objects.order_by('id'))
    current_index = all_videos.index(video)
    next_video = all_videos[(current_index + 1) % len(all_videos)]
    prev_video = all_videos[(current_index - 1) % len(all_videos)]

    context = {
        'video': video,
        'suggested_videos': videos,
        'next_video': next_video,
        'prev_video': prev_video,
    }
    return render(request, 'videos/video_page.html', context)
