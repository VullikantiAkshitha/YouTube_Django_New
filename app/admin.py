# from django.contrib import admin
# from .models import Video, Comment

# # Unregister Video if already registered
# # try:
# #     admin.site.unregister(Video)
# # except admin.sites.NotRegistered:
# #     pass

# # Register Video
# @admin.register(Video)
# class VideoAdmin(admin.ModelAdmin):
#     list_display = ('title', 'uploaded_by', 'uploaded_at', 'views')

# # Unregister Comment if already registered
# try:
#     admin.site.unregister(Comment)
# except admin.sites.NotRegistered:
#     pass

# # Register Comment
# @admin.register(Comment)
# class CommentAdmin(admin.ModelAdmin):
#     list_display = ('video', 'user', 'created_at')
#     # Remove 'parent' if it's causing errors
#     # You can add it later if the field exists properly

# from django.contrib import admin
# from .models import Video, Comment

# # Unregister if already registered
# for model in [Video, Comment]:
#     try:
#         admin.site.unregister(model)
#     except admin.sites.NotRegistered:
#         pass

from django.contrib import admin
from .models import Video, Comment


admin.site.register(Video)