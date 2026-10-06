from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = "ADMIN", "مدیر سیستم"
        MANAGER = "MANAGER", "مدیر مدرسه"
        TEACHER = "TEACHER", "معلم"
        STUDENT = "STUDENT", "دانش‌آموز"
        PARENT = "PARENT", "والدین"

    role = models.CharField(max_length=10, choices=Role.choices, default=Role.STUDENT, verbose_name="نقش")
    phone_number = models.CharField(max_length=15, blank=True, verbose_name="شماره تماس")
    national_code = models.CharField(max_length=10, blank=True, verbose_name="کد ملی")
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True, verbose_name="تصویر پروفایل")

    def is_admin(self):
        return self.role == self.Role.ADMIN or self.is_superuser

    def is_manager(self):
        return self.role == self.Role.MANAGER

    def is_teacher(self):
        return self.role == self.Role.TEACHER

    def is_student(self):
        return self.role == self.Role.STUDENT

    def is_parent(self):
        return self.role == self.Role.PARENT

    def __str__(self):
        return f"{self.get_full_name() or self.username} ({self.get_role_display()})"

    class Meta:
        verbose_name = "کاربر"
        verbose_name_plural = "کاربران"
