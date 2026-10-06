from django import forms
from core.forms import BootstrapFormMixin
from .models import Attendance
from academics.models import StudentProfile


class AttendanceDateClassForm(BootstrapFormMixin, forms.Form):
    """فرم انتخاب کلاس و تاریخ برای شروع حضور و غیاب"""
    from academics.models import SchoolClass
    school_class = forms.ModelChoiceField(queryset=SchoolClass.objects.all(), label="کلاس")
    date = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}), label="تاریخ")


class SingleAttendanceForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ("status", "note")
