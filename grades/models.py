from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from academics.models import StudentProfile, Subject, TeacherProfile


class Grade(models.Model):
    class GradeType(models.TextChoices):
        QUIZ = "QUIZ", "کوئیز"
        MIDTERM = "MIDTERM", "میان‌ترم"
        FINAL = "FINAL", "پایان‌ترم"
        HOMEWORK = "HOMEWORK", "تکلیف"
        CLASS_ACTIVITY = "CLASS_ACTIVITY", "فعالیت کلاسی"

    class Term(models.TextChoices):
        FIRST = "FIRST", "نیم‌سال اول"
        SECOND = "SECOND", "نیم‌سال دوم"

    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name="grades", verbose_name="دانش‌آموز")
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name="grades", verbose_name="درس")
    teacher = models.ForeignKey(TeacherProfile, on_delete=models.SET_NULL, null=True, related_name="grades", verbose_name="معلم")
    grade_type = models.CharField(max_length=20, choices=GradeType.choices, default=GradeType.QUIZ, verbose_name="نوع نمره")
    term = models.CharField(max_length=10, choices=Term.choices, default=Term.FIRST, verbose_name="نیم‌سال")
    score = models.DecimalField(
        max_digits=4, decimal_places=2, verbose_name="نمره",
        validators=[MinValueValidator(0), MaxValueValidator(20)]
    )
    max_score = models.DecimalField(max_digits=4, decimal_places=2, default=20, verbose_name="نمره کامل")
    date = models.DateField(verbose_name="تاریخ ثبت")
    comment = models.CharField(max_length=255, blank=True, verbose_name="توضیح معلم")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "نمره"
        verbose_name_plural = "نمرات"
        ordering = ["-date"]

    def __str__(self):
        return f"{self.student} - {self.subject} - {self.score}"
