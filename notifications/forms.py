from django import forms
from core.forms import BootstrapFormMixin
from .models import Announcement, DirectMessage


class AnnouncementForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Announcement
        fields = ("title", "content", "audience", "school_class", "is_pinned")
        widgets = {"content": forms.Textarea(attrs={"rows": 5})}


class DirectMessageForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = DirectMessage
        fields = ("recipient", "body")
        widgets = {"body": forms.Textarea(attrs={"rows": 4})}
