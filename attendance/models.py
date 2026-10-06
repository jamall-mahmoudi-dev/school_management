from django.db import models
from django.conf import settings
from academics.models import StudentProfile, TimetableEntry, SchoolClass


class Attendance(models.Model):
    class Status(models.TextChoices):
        PRESENT = "PRESENT", "حاضر"
        ABSENT = "ABSENT", "غایب"
        LATE = "LATE", "با تاخیر"
        EXCUSED = "EXCUSED", "غیبت موجه"

    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name="attendances", verbose_name="دانش‌آموز")
    timetable_entry = models.ForeignKey(
        TimetableEntry, on_delete=models.CASCADE, related_name="attendances",
        null=True, blank=True, verbose_name="جلسه درسی"
    )
    school_class = models.ForeignKey(SchoolClass, on_delete=models.CASCADE, related_name="attendances", verbose_name="کلاس")
    date = models.DateField(verbose_name="تاریخ")
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PRESENT, verbose_name="وضعیت")
    note = models.CharField(max_length=255, blank=True, verbose_name="توضیح")
    recorded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="recorded_attendances",
        verbose_name="ثبت شده توسط"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "حضور و غیاب"
        verbose_name_plural = "حضور و غیاب"
        ordering = ["-date"]
        unique_together = ("student", "timetable_entry", "date")

    def __str__(self):
        return f"{self.student} - {self.date} - {self.get_status_display()}"
