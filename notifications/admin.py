from django.contrib import admin
from .models import Announcement, DirectMessage


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ("title", "audience", "school_class", "created_by", "is_pinned", "created_at")
    list_filter = ("audience", "is_pinned")
    search_fields = ("title", "content")


@admin.register(DirectMessage)
class DirectMessageAdmin(admin.ModelAdmin):
    list_display = ("sender", "recipient", "is_read", "created_at")
    list_filter = ("is_read",)
