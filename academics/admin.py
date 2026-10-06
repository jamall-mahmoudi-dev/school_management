from django.contrib import admin
from .models import SchoolClass, Subject, TeacherProfile, StudentProfile, ParentProfile, TimetableEntry


@admin.register(SchoolClass)
class SchoolClassAdmin(admin.ModelAdmin):
    list_display = ("name", "grade_level", "section", "homeroom_teacher", "student_count", "academic_year")
    list_filter = ("grade_level", "academic_year")
    search_fields = ("name",)


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ("name", "code", "weekly_hours")
    search_fields = ("name", "code")


@admin.register(TeacherProfile)
class TeacherProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "hire_date")
    filter_horizontal = ("subjects",)
    search_fields = ("user__first_name", "user__last_name", "user__username")


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "student_number", "school_class", "birth_date")
    list_filter = ("school_class",)
    search_fields = ("user__first_name", "user__last_name", "student_number")


@admin.register(ParentProfile)
class ParentProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "relation")
    filter_horizontal = ("children",)


@admin.register(TimetableEntry)
class TimetableEntryAdmin(admin.ModelAdmin):
    list_display = ("school_class", "subject", "teacher", "weekday", "start_time", "end_time")
    list_filter = ("school_class", "weekday")
