from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.utils import timezone
from django.views import View

from academics.models import SchoolClass, Subject, TeacherProfile, StudentProfile, TimetableEntry
from attendance.models import Attendance
from grades.models import Grade
from notifications.models import Announcement


def home(request):
    if request.user.is_authenticated:
        return redirect("core:dashboard")
    return render(request, "core/home.html")


class DashboardView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        context = {"today": timezone.localdate()}

        if user.is_superuser or user.is_admin() or user.is_manager():
            context.update({
                "role_template": "core/dashboard_manager.html",
                "total_students": StudentProfile.objects.count(),
                "total_teachers": TeacherProfile.objects.count(),
                "total_classes": SchoolClass.objects.count(),
                "total_subjects": Subject.objects.count(),
                "announcements": Announcement.objects.all()[:5],
                "classes": SchoolClass.objects.all()[:8],
            })
        elif user.is_teacher():
            teacher_profile = getattr(user, "teacher_profile", None)
            todays_classes = []
            if teacher_profile:
                weekday = timezone.localdate().weekday()
                # Convert python weekday (Mon=0) to our Saturday=0 scheme
                weekday = (weekday + 2) % 7
                todays_classes = TimetableEntry.objects.filter(teacher=teacher_profile, weekday=weekday)
            context.update({
                "role_template": "core/dashboard_teacher.html",
                "teacher_profile": teacher_profile,
                "todays_classes": todays_classes,
                "announcements": Announcement.objects.filter(audience__in=["ALL", "TEACHERS"])[:5],
                "homeroom_classes": teacher_profile.homeroom_classes.all() if teacher_profile else [],
            })
        elif user.is_student():
            student_profile = getattr(user, "student_profile", None)
            recent_grades = Grade.objects.filter(student=student_profile)[:5] if student_profile else []
            recent_attendance = Attendance.objects.filter(student=student_profile)[:5] if student_profile else []
            context.update({
                "role_template": "core/dashboard_student.html",
                "student_profile": student_profile,
                "recent_grades": recent_grades,
                "recent_attendance": recent_attendance,
                "announcements": Announcement.objects.filter(audience__in=["ALL", "STUDENTS"])[:5],
            })
        elif user.is_parent():
            parent_profile = getattr(user, "parent_profile", None)
            children = parent_profile.children.all() if parent_profile else []
            context.update({
                "role_template": "core/dashboard_parent.html",
                "parent_profile": parent_profile,
                "children": children,
                "announcements": Announcement.objects.filter(audience__in=["ALL", "PARENTS"])[:5],
            })
        else:
            context["role_template"] = "core/dashboard_manager.html"

        return render(request, "core/dashboard.html", context)
