from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Channel, Video, Comment


# Create your views here.
def home(request):
    videos = Video.objects.all().order_by("-upload_time")
    user_channel = None
    if request.user.is_authenticated:
        user_channel = Channel.objects.filter(user=request.user).first()
    return render(request, "home.html", {
        "videos": videos,
        "user_channel": user_channel
    })


def create_channel(request):
    if request.method == "POST":
        name = request.POST.get("channelName")
        pfp = request.FILES.get("channel_pfp")

        if not name:
            messages.error(request, "Channel name is required.")
            return render(request, "create_channel.html")

        channel = Channel(
            user=request.user,
            name=name,
            profile_picture=pfp if pfp else "images/default_pfp.png",
        )
        channel.save()
        messages.success(request, "Channel created successfully!")
        return redirect("home")

    return render(request, "create_channel.html")


def video(request, pk):
    video = Video.objects.get(id=pk)
    return render(request, "video.html", {"video": video})


def create_user(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
    else:
        form = UserCreationForm()

    return render(request, "create_user.html", {"form": form})


def custom_login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            return redirect("login")

    else:
        return render(request, "login.html")


def custom_logout(request):
    logout(request)
    return redirect("home")


def channel(request, username, pk):
    channel = get_object_or_404(Channel,user__username=username, pk=pk)

    if not channel:
        return redirect("create-channel")
    # Optional: verify that the username in the URL matches the channel's owner
    if channel.user.username != username:
        return render(request, "404.html", status=404)
    
    context = {
        "channel": channel,
        "videos": channel.video_set.all(),  # Assuming a related name from a Video model
    }
    return render(request, "channel.html", context)


def upload_video(request):
    if not request.user.is_authenticated:
        return redirect("login")

    channels = Channel.objects.filter(user=request.user)

    if request.method == "POST":
        channel_id = request.POST.get("video_channel")
        video_file = request.FILES.get("video_file")
        title = request.POST.get("video_title")
        description = request.POST.get("video_description")
        thumbnail = request.FILES.get("video_thumbnail")

        # 🧩 Validation
        if not channel_id:
            return render(
                request,
                "upload_video.html",
                {"channels": channels, "error": "Please select a channel."},
            )

        try:
            # 🧩 Only allow user's own channels
            channel = Channel.objects.get(id=channel_id, user=request.user)
        except Channel.DoesNotExist:
            return render(
                request,
                "upload_video.html",
                {
                    "channels": channels,
                    "error": "Selected channel does not exist or is not yours.",
                },
            )

        if not (video_file and title and thumbnail):
            return render(
                request,
                "upload_video.html",
                {"channels": channels, "error": "All fields are required."},
            )

        # 🧩 Create video
        video = Video.objects.create(
            user=request.user,
            channel=channel,
            video_file=video_file,
            title=title,
            description=description,
            thumbnail=thumbnail,
        )

        return redirect("home")

    # GET request — render upload form
    return render(request, "upload_video.html", {"channels": channels})


def searched(request):
    if request.method == "POST":
        searched_value = request.POST["s"]
        videos = Video.objects.filter(title__contains=searched_value)
        channels = Channel.objects.filter(name__contains=searched_value)

        return render(
            request, "searched.html", {"videos": videos, "channels": channels}
        )


def video_view(request, pk):
    if request.user.is_authenticated:
        video = Video.objects.get(id=pk)

        if not video.view.filter(id=request.user.id):
            video.view.add(request.user)

        return redirect("video", pk=pk)
    else:
        return redirect("login")


def video_like(request, pk):
    if request.user.is_authenticated:
        video = Video.objects.get(id=pk)

        if not video.dislikes.filter(id=request.user.id):
            if video.likes.filter(id=request.user.id):
                video.likes.remove(request.user)
            else:
                video.likes.add(request.user)

        return redirect("video", pk=pk)

    else:
        return redirect("login")


def video_dislike(request, pk):
    if request.user.is_authenticated:
        video = Video.objects.get(id=pk)

        if not video.likes.filter(id=request.user.id):
            if video.dislikes.filter(id=request.user.id):
                video.dislikes.remove(request.user)
            else:
                video.dislikes.add(request.user)

        return redirect("video", pk=pk)

    else:
        return redirect("login")


def video_comment(request, pk):
    if request.user.is_authenticated:
        video = Video.objects.get(id=pk)

        if request.method == "POST":
            comment_text = request.POST["comment"]
            comment = Comment.objects.create(
                user=request.user, video=video, text=comment_text
            )

        return redirect("video", pk=pk)

    else:
        return redirect("login")
