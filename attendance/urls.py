from django.urls import path
from . import views

app_name = "attendance"

urlpatterns = [
    path("select/", views.AttendanceSelectView.as_view(), name="select"),
    path("take/<int:class_id>/", views.AttendanceTakeView.as_view(), name="take"),
    path("my/", views.MyAttendanceView.as_view(), name="my"),
    path("my/<int:student_id>/", views.MyAttendanceView.as_view(), name="my_child"),
    path("report/<int:class_id>/", views.ClassAttendanceReportView.as_view(), name="class_report"),
]
