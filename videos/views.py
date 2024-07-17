from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Video
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

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

    next_video = None
    prev_video = None
    has_next = False
    has_prev = False

    if current_index < len(all_videos) - 1:
        next_video = all_videos[current_index + 1]
        has_next = True

    if current_index > 0:
        prev_video = all_videos[current_index - 1]
        has_prev = True

    context = {
        'video': video,
        'suggested_videos': videos,
        'next_video': next_video,
        'prev_video': prev_video,
        'has_next': has_next,
        'has_prev': has_prev,
    }
    return render(request, 'videos/video_page.html', context)

@csrf_exempt
@require_POST
def increment_view(request, slug):
    video = get_object_or_404(Video, slug=slug)
    video.views += 1
    video.save()
    return JsonResponse({'status': 'ok'})