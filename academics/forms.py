from django import forms
from core.forms import BootstrapFormMixin
from .models import SchoolClass, Subject, TimetableEntry


class SchoolClassForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = SchoolClass
        fields = ("name", "grade_level", "section", "capacity", "homeroom_teacher", "academic_year")


class SubjectForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Subject
        fields = ("name", "code", "weekly_hours", "description")
        widgets = {"description": forms.Textarea(attrs={"rows": 3})}


class TimetableEntryForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = TimetableEntry
        fields = ("school_class", "subject", "teacher", "weekday", "start_time", "end_time")
        widgets = {
            "start_time": forms.TimeInput(attrs={"type": "time"}),
            "end_time": forms.TimeInput(attrs={"type": "time"}),
        }
