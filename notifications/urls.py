from django.urls import path
from . import views

app_name = "notifications"

urlpatterns = [
    path("", views.AnnouncementListView.as_view(), name="announcement_list"),
    path("add/", views.AnnouncementCreateView.as_view(), name="announcement_add"),
    path("<int:pk>/delete/", views.AnnouncementDeleteView.as_view(), name="announcement_delete"),
    path("inbox/", views.InboxView.as_view(), name="inbox"),
]
