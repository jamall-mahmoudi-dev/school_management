from django.contrib import messages
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DeleteView
from django.views import View

from core.mixins import RoleRequiredMixin
from .models import Announcement, DirectMessage
from .forms import AnnouncementForm, DirectMessageForm

CREATE_ROLES = ["ADMIN", "MANAGER", "TEACHER"]

AUDIENCE_BY_ROLE = {
    "STUDENT": ["ALL", "STUDENTS"],
    "TEACHER": ["ALL", "TEACHERS"],
    "PARENT": ["ALL", "PARENTS"],
    "MANAGER": ["ALL", "TEACHERS", "STUDENTS", "PARENTS", "CLASS"],
    "ADMIN": ["ALL", "TEACHERS", "STUDENTS", "PARENTS", "CLASS"],
}


class AnnouncementListView(RoleRequiredMixin, ListView):
    model = Announcement
    template_name = "notifications/announcement_list.html"
    context_object_name = "announcements"
    allowed_roles = ["ADMIN", "MANAGER", "TEACHER", "STUDENT", "PARENT"]

    def get_queryset(self):
        user = self.request.user
        role = "ADMIN" if (user.is_superuser or user.is_admin()) else user.role
        audiences = AUDIENCE_BY_ROLE.get(role, ["ALL"])
        qs = Announcement.objects.filter(audience__in=audiences)
        if user.is_student() and hasattr(user, "student_profile"):
            qs = qs | Announcement.objects.filter(audience="CLASS", school_class=user.student_profile.school_class)
        return qs.distinct()


class AnnouncementCreateView(RoleRequiredMixin, CreateView):
    model = Announcement
    form_class = AnnouncementForm
    template_name = "notifications/announcement_form.html"
    allowed_roles = CREATE_ROLES
    success_url = reverse_lazy("notifications:announcement_list")

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        messages.success(self.request, "اطلاعیه با موفقیت منتشر شد.")
        return super().form_valid(form)


class AnnouncementDeleteView(RoleRequiredMixin, DeleteView):
    model = Announcement
    template_name = "notifications/announcement_confirm_delete.html"
    allowed_roles = CREATE_ROLES
    success_url = reverse_lazy("notifications:announcement_list")


class InboxView(RoleRequiredMixin, View):
    allowed_roles = ["ADMIN", "MANAGER", "TEACHER", "STUDENT", "PARENT"]
    template_name = "notifications/inbox.html"

    def get(self, request):
        messages_qs = DirectMessage.objects.filter(
            Q(recipient=request.user) | Q(sender=request.user)
        ).select_related("sender", "recipient")
        DirectMessage.objects.filter(recipient=request.user, is_read=False).update(is_read=True)
        return render(request, self.template_name, {"messages_list": messages_qs, "form": DirectMessageForm()})

    def post(self, request):
        form = DirectMessageForm(request.POST)
        if form.is_valid():
            dm = form.save(commit=False)
            dm.sender = request.user
            dm.save()
            messages.success(request, "پیام ارسال شد.")
        return redirect("notifications:inbox")
