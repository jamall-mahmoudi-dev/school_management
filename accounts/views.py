from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DeleteView, UpdateView, DetailView
from django.views import View
from django.shortcuts import render

from core.mixins import RoleRequiredMixin
from .forms import (
    StyledAuthenticationForm, ManagerCreateForm, TeacherCreateForm, StudentCreateForm, ParentCreateForm,
    UserUpdateForm, TeacherProfileForm, StudentProfileForm, ParentProfileForm,
)
from .models import User


class StyledLoginView(LoginView):
    template_name = "accounts/login.html"
    authentication_form = StyledAuthenticationForm
    redirect_authenticated_user = True


class StyledLogoutView(LogoutView):
    next_page = "accounts:login"


class UserListView(RoleRequiredMixin, ListView):
    model = User
    template_name = "accounts/user_list.html"
    context_object_name = "users"
    paginate_by = 20
    allowed_roles = ["ADMIN", "MANAGER"]

    def get_queryset(self):
        qs = User.objects.all().order_by("role", "first_name")
        role = self.request.GET.get("role")
        q = self.request.GET.get("q")
        if role:
            qs = qs.filter(role=role)
        if q:
            qs = qs.filter(first_name__icontains=q) | qs.filter(last_name__icontains=q) | qs.filter(username__icontains=q)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["roles"] = User.Role.choices
        ctx["selected_role"] = self.request.GET.get("role", "")
        return ctx


class UserDetailView(RoleRequiredMixin, DetailView):
    model = User
    template_name = "accounts/user_detail.html"
    context_object_name = "person"
    allowed_roles = ["ADMIN", "MANAGER"]


FORM_MAP = {
    "MANAGER": (ManagerCreateForm, "مدیر مدرسه"),
    "TEACHER": (TeacherCreateForm, "معلم"),
    "STUDENT": (StudentCreateForm, "دانش‌آموز"),
    "PARENT": (ParentCreateForm, "والدین"),
}


class UserCreateView(RoleRequiredMixin, View):
    allowed_roles = ["ADMIN", "MANAGER"]
    template_name = "accounts/user_form.html"

    def get(self, request, role):
        form_class, label = FORM_MAP.get(role.upper(), (None, None))
        if not form_class:
            messages.error(request, "نقش نامعتبر است.")
            return redirect("accounts:user_list")
        return render(request, self.template_name, {"form": form_class(), "role_label": label})

    def post(self, request, role):
        form_class, label = FORM_MAP.get(role.upper(), (None, None))
        if not form_class:
            messages.error(request, "نقش نامعتبر است.")
            return redirect("accounts:user_list")
        form = form_class(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f"{label} «{user.get_full_name()}» با موفقیت اضافه شد.")
            return redirect("accounts:user_list")
        return render(request, self.template_name, {"form": form, "role_label": label})


class UserUpdateView(RoleRequiredMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = "accounts/user_edit.html"
    allowed_roles = ["ADMIN", "MANAGER"]
    success_url = reverse_lazy("accounts:user_list")

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        target = self.object
        profile_form = None
        if target.role == User.Role.TEACHER and hasattr(target, "teacher_profile"):
            profile_form = TeacherProfileForm(instance=target.teacher_profile)
        elif target.role == User.Role.STUDENT and hasattr(target, "student_profile"):
            profile_form = StudentProfileForm(instance=target.student_profile)
        elif target.role == User.Role.PARENT and hasattr(target, "parent_profile"):
            profile_form = ParentProfileForm(instance=target.parent_profile)
        ctx["profile_form"] = profile_form
        return ctx

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        target = self.object
        profile_instance = None
        profile_form_class = None
        if target.role == User.Role.TEACHER and hasattr(target, "teacher_profile"):
            profile_instance, profile_form_class = target.teacher_profile, TeacherProfileForm
        elif target.role == User.Role.STUDENT and hasattr(target, "student_profile"):
            profile_instance, profile_form_class = target.student_profile, StudentProfileForm
        elif target.role == User.Role.PARENT and hasattr(target, "parent_profile"):
            profile_instance, profile_form_class = target.parent_profile, ParentProfileForm

        profile_form = profile_form_class(request.POST, instance=profile_instance) if profile_form_class else None

        if form.is_valid() and (profile_form is None or profile_form.is_valid()):
            form.save()
            if profile_form:
                profile_form.save()
            messages.success(request, "اطلاعات با موفقیت به‌روزرسانی شد.")
            return redirect(self.success_url)
        return self.render_to_response(self.get_context_data(form=form, profile_form=profile_form))


class UserDeleteView(RoleRequiredMixin, DeleteView):
    model = User
    template_name = "accounts/user_confirm_delete.html"
    allowed_roles = ["ADMIN", "MANAGER"]
    success_url = reverse_lazy("accounts:user_list")

    def form_valid(self, form):
        messages.success(self.request, "کاربر با موفقیت حذف شد.")
        return super().form_valid(form)
