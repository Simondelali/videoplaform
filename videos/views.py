from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Video , Comment
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages

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
    comments = video.comments.filter(parent=None)

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
        'comments': comments,
    }
    return render(request, 'videos/video_page.html', context)

@csrf_exempt
@require_POST
def increment_view(request, slug):
    video = get_object_or_404(Video, slug=slug)
    video.views += 1
    video.save()
    return JsonResponse({'status': 'ok'})

@login_required
def post_comment(request, slug):
    if request.method == 'POST':
        video = get_object_or_404(Video, slug=slug)
        content = request.POST.get('content')
        if content:
            Comment.objects.create(video=video, user=request.user, content=content)
            messages.success(request, 'Comment posted successfully.')
        else:
            messages.error(request, 'Comment cannot be empty.')
    return redirect('video_page', slug=slug)

@login_required
def post_reply(request, slug, comment_id):
    if request.method == 'POST':
        video = get_object_or_404(Video, slug=slug)
        parent_comment = get_object_or_404(Comment, id=comment_id, video=video)
        content = request.POST.get('content')
        if content:
            Comment.objects.create(video=video, user=request.user, content=content, parent=parent_comment)
            messages.success(request, 'Reply posted successfully.')
        else:
            messages.error(request, 'Reply cannot be empty.')
    return redirect('video_page', slug=slug)

@login_required
def delete_comment(request, slug, comment_id):
    if request.method == 'POST':
        comment = get_object_or_404(Comment, id=comment_id, video__slug=slug)
        if request.user == comment.user:
            comment.delete()
            messages.success(request, 'Comment deleted successfully.')
        else:
            messages.error(request, 'You do not have permission to delete this comment.')
    return redirect('video_page', slug=slug)