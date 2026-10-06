from django import forms
from core.forms import BootstrapFormMixin
from .models import Grade


class GradeForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Grade
        fields = ("student", "subject", "grade_type", "term", "score", "max_score", "date", "comment")
        widgets = {"date": forms.DateInput(attrs={"type": "date"})}
