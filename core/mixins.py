from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied


class RoleRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """
    محدود کردن دسترسی به یک ویو بر اساس نقش کاربر.
    در ویو باید allowed_roles = ["ADMIN", "MANAGER", ...] تعریف شود.
    """
    allowed_roles = []
    raise_exception = True

    def test_func(self):
        user = self.request.user
        if not user.is_authenticated:
            return False
        if user.is_superuser or user.role == "ADMIN":
            return True
        return user.role in self.allowed_roles

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return super().handle_no_permission()
        raise PermissionDenied("شما به این بخش دسترسی ندارید.")
