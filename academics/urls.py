from django.urls import path
from . import views

app_name = "academics"

urlpatterns = [
    path("classes/", views.SchoolClassListView.as_view(), name="class_list"),
    path("classes/add/", views.SchoolClassCreateView.as_view(), name="class_add"),
    path("classes/<int:pk>/", views.SchoolClassDetailView.as_view(), name="class_detail"),
    path("classes/<int:pk>/edit/", views.SchoolClassUpdateView.as_view(), name="class_edit"),
    path("classes/<int:pk>/delete/", views.SchoolClassDeleteView.as_view(), name="class_delete"),

    path("subjects/", views.SubjectListView.as_view(), name="subject_list"),
    path("subjects/add/", views.SubjectCreateView.as_view(), name="subject_add"),
    path("subjects/<int:pk>/edit/", views.SubjectUpdateView.as_view(), name="subject_edit"),
    path("subjects/<int:pk>/delete/", views.SubjectDeleteView.as_view(), name="subject_delete"),

    path("timetable/add/", views.TimetableEntryCreateView.as_view(), name="timetable_add"),
    path("timetable/<int:pk>/delete/", views.TimetableEntryDeleteView.as_view(), name="timetable_delete"),
]
