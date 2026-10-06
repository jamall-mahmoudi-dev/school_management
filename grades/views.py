from django.contrib import messages
from django.db.models import Avg
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.views import View

from core.mixins import RoleRequiredMixin
from academics.models import SchoolClass, StudentProfile, TeacherProfile
from .models import Grade
from .forms import GradeForm

TEACH_ROLES = ["ADMIN", "MANAGER", "TEACHER"]


class GradeListView(RoleRequiredMixin, ListView):
    model = Grade
    template_name = "grades/grade_list.html"
    context_object_name = "grades"
    allowed_roles = TEACH_ROLES
    paginate_by = 30

    def get_queryset(self):
        qs = Grade.objects.select_related("student__user", "subject", "teacher__user").all()
        class_id = self.request.GET.get("class")
        subject_id = self.request.GET.get("subject")
        if class_id:
            qs = qs.filter(student__school_class_id=class_id)
        if subject_id:
            qs = qs.filter(subject_id=subject_id)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["classes"] = SchoolClass.objects.all()
        return ctx


class GradeCreateView(RoleRequiredMixin, CreateView):
    model = Grade
    form_class = GradeForm
    template_name = "grades/grade_form.html"
    allowed_roles = TEACH_ROLES
    success_url = reverse_lazy("grades:grade_list")

    def form_valid(self, form):
        if self.request.user.is_teacher():
            form.instance.teacher = getattr(self.request.user, "teacher_profile", None)
        messages.success(self.request, "نمره با موفقیت ثبت شد.")
        return super().form_valid(form)


class GradeUpdateView(RoleRequiredMixin, UpdateView):
    model = Grade
    form_class = GradeForm
    template_name = "grades/grade_form.html"
    allowed_roles = TEACH_ROLES
    success_url = reverse_lazy("grades:grade_list")


class GradeDeleteView(RoleRequiredMixin, DeleteView):
    model = Grade
    template_name = "grades/grade_confirm_delete.html"
    allowed_roles = TEACH_ROLES
    success_url = reverse_lazy("grades:grade_list")


class MyReportCardView(RoleRequiredMixin, View):
    allowed_roles = ["STUDENT", "PARENT"]
    template_name = "grades/report_card.html"

    def get(self, request, student_id=None):
        user = request.user
        if user.is_student():
            student = get_object_or_404(StudentProfile, user=user)
        else:
            parent_profile = getattr(user, "parent_profile", None)
            student = get_object_or_404(parent_profile.children, pk=student_id) if student_id else (
                parent_profile.children.first() if parent_profile else None
            )

        grades = Grade.objects.filter(student=student).select_related("subject") if student else []
        by_subject = {}
        if student:
            for subject in {g.subject for g in grades}:
                subject_grades = [g for g in grades if g.subject_id == subject.id]
                avg = sum(float(g.score) for g in subject_grades) / len(subject_grades)
                by_subject[subject] = {"grades": subject_grades, "average": round(avg, 2)}

        context = {"student": student, "by_subject": by_subject}
        if user.is_parent():
            context["children"] = getattr(user, "parent_profile", None).children.all() if hasattr(user, "parent_profile") else []
        return render(request, self.template_name, context)
