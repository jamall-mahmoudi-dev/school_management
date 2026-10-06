from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView

from core.mixins import RoleRequiredMixin
from .models import SchoolClass, Subject, TimetableEntry
from .forms import SchoolClassForm, SubjectForm, TimetableEntryForm

MANAGE_ROLES = ["ADMIN", "MANAGER"]


class SchoolClassListView(RoleRequiredMixin, ListView):
    model = SchoolClass
    template_name = "academics/class_list.html"
    context_object_name = "classes"
    allowed_roles = MANAGE_ROLES + ["TEACHER", "STUDENT", "PARENT"]


class SchoolClassDetailView(RoleRequiredMixin, DetailView):
    model = SchoolClass
    template_name = "academics/class_detail.html"
    context_object_name = "school_class"
    allowed_roles = MANAGE_ROLES + ["TEACHER", "STUDENT", "PARENT"]

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["timetable"] = self.object.timetable_entries.select_related("subject", "teacher__user")
        ctx["students"] = self.object.students.select_related("user")
        return ctx


class SchoolClassCreateView(RoleRequiredMixin, CreateView):
    model = SchoolClass
    form_class = SchoolClassForm
    template_name = "academics/class_form.html"
    allowed_roles = MANAGE_ROLES
    success_url = reverse_lazy("academics:class_list")

    def form_valid(self, form):
        messages.success(self.request, "کلاس با موفقیت ایجاد شد.")
        return super().form_valid(form)


class SchoolClassUpdateView(RoleRequiredMixin, UpdateView):
    model = SchoolClass
    form_class = SchoolClassForm
    template_name = "academics/class_form.html"
    allowed_roles = MANAGE_ROLES
    success_url = reverse_lazy("academics:class_list")


class SchoolClassDeleteView(RoleRequiredMixin, DeleteView):
    model = SchoolClass
    template_name = "academics/class_confirm_delete.html"
    allowed_roles = MANAGE_ROLES
    success_url = reverse_lazy("academics:class_list")


class SubjectListView(RoleRequiredMixin, ListView):
    model = Subject
    template_name = "academics/subject_list.html"
    context_object_name = "subjects"
    allowed_roles = MANAGE_ROLES + ["TEACHER", "STUDENT", "PARENT"]


class SubjectCreateView(RoleRequiredMixin, CreateView):
    model = Subject
    form_class = SubjectForm
    template_name = "academics/subject_form.html"
    allowed_roles = MANAGE_ROLES
    success_url = reverse_lazy("academics:subject_list")


class SubjectUpdateView(RoleRequiredMixin, UpdateView):
    model = Subject
    form_class = SubjectForm
    template_name = "academics/subject_form.html"
    allowed_roles = MANAGE_ROLES
    success_url = reverse_lazy("academics:subject_list")


class SubjectDeleteView(RoleRequiredMixin, DeleteView):
    model = Subject
    template_name = "academics/subject_confirm_delete.html"
    allowed_roles = MANAGE_ROLES
    success_url = reverse_lazy("academics:subject_list")


class TimetableEntryCreateView(RoleRequiredMixin, CreateView):
    model = TimetableEntry
    form_class = TimetableEntryForm
    template_name = "academics/timetable_form.html"
    allowed_roles = MANAGE_ROLES

    def get_initial(self):
        initial = super().get_initial()
        class_id = self.request.GET.get("class")
        if class_id:
            initial["school_class"] = class_id
        return initial

    def get_success_url(self):
        return reverse_lazy("academics:class_detail", kwargs={"pk": self.object.school_class_id})


class TimetableEntryDeleteView(RoleRequiredMixin, DeleteView):
    model = TimetableEntry
    template_name = "academics/timetable_confirm_delete.html"
    allowed_roles = MANAGE_ROLES

    def get_success_url(self):
        return reverse_lazy("academics:class_detail", kwargs={"pk": self.object.school_class_id})
