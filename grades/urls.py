from django.urls import path
from . import views

app_name = "grades"

urlpatterns = [
    path("", views.GradeListView.as_view(), name="grade_list"),
    path("add/", views.GradeCreateView.as_view(), name="grade_add"),
    path("<int:pk>/edit/", views.GradeUpdateView.as_view(), name="grade_edit"),
    path("<int:pk>/delete/", views.GradeDeleteView.as_view(), name="grade_delete"),
    path("report-card/", views.MyReportCardView.as_view(), name="report_card"),
    path("report-card/<int:student_id>/", views.MyReportCardView.as_view(), name="report_card_child"),
]
