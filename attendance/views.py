from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils import timezone
from django.views import View

from core.mixins import RoleRequiredMixin
from academics.models import SchoolClass, StudentProfile
from .models import Attendance

TAKE_ROLES = ["ADMIN", "MANAGER", "TEACHER"]


class AttendanceSelectView(RoleRequiredMixin, View):
    allowed_roles = TAKE_ROLES
    template_name = "attendance/select.html"

    def get(self, request):
        classes = SchoolClass.objects.all()
        return render(request, self.template_name, {"classes": classes, "today": timezone.localdate()})


class AttendanceTakeView(RoleRequiredMixin, View):
    allowed_roles = TAKE_ROLES
    template_name = "attendance/take.html"

    def get(self, request, class_id):
        school_class = get_object_or_404(SchoolClass, pk=class_id)
        date_str = request.GET.get("date") or str(timezone.localdate())
        students = school_class.students.select_related("user").all()
        existing = {a.student_id: a for a in Attendance.objects.filter(school_class=school_class, date=date_str)}
        rows = [
            {"student": s, "status": existing[s.id].status if s.id in existing else "PRESENT",
             "note": existing[s.id].note if s.id in existing else ""}
            for s in students
        ]
        return render(request, self.template_name, {
            "school_class": school_class, "rows": rows, "date": date_str,
            "status_choices": Attendance.Status.choices,
        })

    def post(self, request, class_id):
        school_class = get_object_or_404(SchoolClass, pk=class_id)
        date_str = request.POST.get("date")
        students = school_class.students.all()
        for s in students:
            status = request.POST.get(f"status_{s.id}", "PRESENT")
            note = request.POST.get(f"note_{s.id}", "")
            Attendance.objects.update_or_create(
                student=s, school_class=school_class, date=date_str, timetable_entry=None,
                defaults={"status": status, "note": note, "recorded_by": request.user},
            )
        messages.success(request, f"حضور و غیاب کلاس {school_class} برای تاریخ {date_str} ثبت شد.")
        return redirect(f"{reverse('attendance:take', args=[class_id])}?date={date_str}")


class MyAttendanceView(RoleRequiredMixin, View):
    allowed_roles = ["STUDENT", "PARENT"]
    template_name = "attendance/my_attendance.html"

    def get(self, request, student_id=None):
        user = request.user
        if user.is_student():
            student = get_object_or_404(StudentProfile, user=user)
        else:
            parent_profile = getattr(user, "parent_profile", None)
            if student_id:
                student = get_object_or_404(parent_profile.children, pk=student_id)
            else:
                student = parent_profile.children.first() if parent_profile else None

        records = Attendance.objects.filter(student=student).select_related("school_class") if student else []
        summary = {}
        if student:
            for key, label in Attendance.Status.choices:
                summary[label] = records.filter(status=key).count()

        context = {"student": student, "records": records[:60], "summary": summary}
        if user.is_parent():
            context["children"] = getattr(user, "parent_profile", None).children.all() if hasattr(user, "parent_profile") else []
        return render(request, self.template_name, context)


class ClassAttendanceReportView(RoleRequiredMixin, View):
    allowed_roles = ["ADMIN", "MANAGER", "TEACHER"]
    template_name = "attendance/class_report.html"

    def get(self, request, class_id):
        school_class = get_object_or_404(SchoolClass, pk=class_id)
        students = school_class.students.select_related("user")
        report = []
        for s in students:
            qs = Attendance.objects.filter(student=s)
            report.append({
                "student": s,
                "present": qs.filter(status="PRESENT").count(),
                "absent": qs.filter(status="ABSENT").count(),
                "late": qs.filter(status="LATE").count(),
                "excused": qs.filter(status="EXCUSED").count(),
            })
        return render(request, self.template_name, {"school_class": school_class, "report": report})
