from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('channel/<str:username>/<int:pk>', views.channel, name='channel'),
    path('video/<int:pk>', views.video, name='video'),

    path('create-user', views.create_user, name='create-user'),
    path('login', views.custom_login, name='login'),
    path('logout', views.custom_logout, name='logout'),
    path('upload-video', views.upload_video, name='upload-video'),
    path('create-channel/', views.create_channel, name='create-channel'),
    path('searched', views.searched, name='searched'),

    path('video-view/<int:pk>', views.video_view, name='video-view'),
    path('video-like/<int:pk>', views.video_like, name='video-like'),
    path('video-dislike/<int:pk>', views.video_dislike, name='video-dislike'),
    path('video-comment/<int:pk>', views.video_comment, name='video-comment'),
    path('video/delete/<int:pk>', views.delete_video, name='delete-video'),
    path('video/update/<int:pk>', views.update_video, name='update-video'),
]