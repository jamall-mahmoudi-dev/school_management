from django.db import models
from django.conf import settings
from academics.models import SchoolClass


class Announcement(models.Model):
    class Audience(models.TextChoices):
        ALL = "ALL", "همه"
        TEACHERS = "TEACHERS", "معلمان"
        STUDENTS = "STUDENTS", "دانش‌آموزان"
        PARENTS = "PARENTS", "والدین"
        CLASS = "CLASS", "یک کلاس خاص"

    title = models.CharField(max_length=200, verbose_name="عنوان")
    content = models.TextField(verbose_name="متن اطلاعیه")
    audience = models.CharField(max_length=10, choices=Audience.choices, default=Audience.ALL, verbose_name="مخاطب")
    school_class = models.ForeignKey(
        SchoolClass, on_delete=models.CASCADE, null=True, blank=True,
        related_name="announcements", verbose_name="کلاس (در صورت مخاطب خاص)"
    )
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="announcements", verbose_name="ایجاد شده توسط")
    is_pinned = models.BooleanField(default=False, verbose_name="سنجاق شده")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ انتشار")

    class Meta:
        verbose_name = "اطلاعیه"
        verbose_name_plural = "اطلاعیه‌ها"
        ordering = ["-is_pinned", "-created_at"]

    def __str__(self):
        return self.title


class DirectMessage(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="sent_messages", verbose_name="فرستنده")
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="received_messages", verbose_name="گیرنده")
    body = models.TextField(verbose_name="متن پیام")
    is_read = models.BooleanField(default=False, verbose_name="خوانده شده")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "پیام مستقیم"
        verbose_name_plural = "پیام‌های مستقیم"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.sender} -> {self.recipient}"
