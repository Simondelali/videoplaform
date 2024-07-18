from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from videos.models import Video
from .forms import VideoForm, VideoEditForm

@staff_member_required
def video_list(request):
    videos = Video.objects.all().order_by('-uploaded_at')
    return render(request, 'customadmin/video_list.html', {'videos': videos})

@staff_member_required
def video_upload(request):
    if request.method == 'POST':
        form = VideoForm(request.POST, request.FILES)
        if form.is_valid():
            video = form.save()
            if video.thumbnail:
                video.process_thumbnail()
            messages.success(request, "Video uploaded successfully.")
            return redirect('customadmin:video_list')
    else:
        form = VideoForm()
    return render(request, 'customadmin/video_form.html', {'form': form, 'title': 'Upload Video'})

@staff_member_required
def video_edit(request, video_id):
    video = get_object_or_404(Video, id=video_id)
    if request.method == 'POST':
        form = VideoEditForm(request.POST, request.FILES, instance=video)
        if form.is_valid():
            video = form.save()
            if video.thumbnail:
                video.process_thumbnail()
            messages.success(request, "Video updated successfully.")
            return redirect('customadmin:video_list')
    else:
        form = VideoEditForm(instance=video)
    return render(request, 'customadmin/video_form.html', {'form': form, 'title': 'Edit Video'})

@staff_member_required
def video_delete(request, video_id):
    video = get_object_or_404(Video, id=video_id)
    if request.method == 'POST':
        video.delete()
        messages.success(request, "Video deleted successfully.")
        return redirect('customadmin:video_list')
    return render(request, 'customadmin/video_delete.html', {'video': video})