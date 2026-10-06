from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


class UserAdmin(BaseUserAdmin):
    list_display = ("username", "first_name", "last_name", "role", "email", "is_active")
    list_filter = ("role", "is_active", "is_staff")
    fieldsets = BaseUserAdmin.fieldsets + (
        ("اطلاعات تکمیلی", {"fields": ("role", "phone_number", "national_code", "avatar")}),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ("اطلاعات تکمیلی", {"fields": ("role", "phone_number", "national_code", "email", "first_name", "last_name")}),
    )


admin.site.register(User, UserAdmin)
admin.site.site_header = "مدیریت دبیرستان"
admin.site.site_title = "پنل مدیریت دبیرستان"
admin.site.index_title = "خوش آمدید"
