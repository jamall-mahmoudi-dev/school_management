from django.contrib import admin
from .models import Grade


@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ("student", "subject", "grade_type", "term", "score", "max_score", "date")
    list_filter = ("grade_type", "term", "subject")
    search_fields = ("student__user__first_name", "student__user__last_name")
    date_hierarchy = "date"
