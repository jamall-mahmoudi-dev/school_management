from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from core.forms import BootstrapFormMixin
from .models import User
from academics.models import TeacherProfile, StudentProfile, ParentProfile, Subject, SchoolClass


class StyledAuthenticationForm(BootstrapFormMixin, AuthenticationForm):
    pass


class BaseUserCreateForm(BootstrapFormMixin, UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "first_name", "last_name", "email", "phone_number", "national_code")


class ManagerCreateForm(BaseUserCreateForm):
    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = User.Role.MANAGER
        if commit:
            user.save()
        return user


class TeacherCreateForm(BaseUserCreateForm):
    subjects = forms.ModelMultipleChoiceField(queryset=Subject.objects.all(), required=False, label="دروس تدریسی")
    hire_date = forms.DateField(required=False, widget=forms.DateInput(attrs={"type": "date"}), label="تاریخ استخدام")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = User.Role.TEACHER
        if commit:
            user.save()
            profile = TeacherProfile.objects.create(user=user, hire_date=self.cleaned_data.get("hire_date"))
            profile.subjects.set(self.cleaned_data.get("subjects"))
        return user


class StudentCreateForm(BaseUserCreateForm):
    student_number = forms.CharField(max_length=20, label="شماره دانش‌آموزی")
    school_class = forms.ModelChoiceField(queryset=SchoolClass.objects.all(), required=False, label="کلاس")
    birth_date = forms.DateField(required=False, widget=forms.DateInput(attrs={"type": "date"}), label="تاریخ تولد")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = User.Role.STUDENT
        if commit:
            user.save()
            StudentProfile.objects.create(
                user=user,
                student_number=self.cleaned_data["student_number"],
                school_class=self.cleaned_data.get("school_class"),
                birth_date=self.cleaned_data.get("birth_date"),
            )
        return user


class ParentCreateForm(BaseUserCreateForm):
    children = forms.ModelMultipleChoiceField(queryset=StudentProfile.objects.all(), required=False, label="فرزندان")
    relation = forms.CharField(max_length=30, initial="پدر/مادر", label="نسبت")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = User.Role.PARENT
        if commit:
            user.save()
            profile = ParentProfile.objects.create(user=user, relation=self.cleaned_data["relation"])
            profile.children.set(self.cleaned_data.get("children"))
        return user


class UserUpdateForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "phone_number", "national_code", "avatar", "is_active")


class TeacherProfileForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = TeacherProfile
        fields = ("subjects", "hire_date", "bio")
        widgets = {"hire_date": forms.DateInput(attrs={"type": "date"})}


class StudentProfileForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = StudentProfile
        fields = ("school_class", "student_number", "birth_date")
        widgets = {"birth_date": forms.DateInput(attrs={"type": "date"})}


class ParentProfileForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = ParentProfile
        fields = ("children", "relation")
