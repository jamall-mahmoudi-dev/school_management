from django.db import models
from django.conf import settings


class SchoolClass(models.Model):
    """کلاس / پایه تحصیلی، مثل: پایه دهم - ریاضی - ۱"""
    name = models.CharField(max_length=100, verbose_name="نام کلاس")
    grade_level = models.PositiveSmallIntegerField(verbose_name="پایه تحصیلی")
    section = models.CharField(max_length=20, blank=True, verbose_name="شعبه")
    capacity = models.PositiveSmallIntegerField(default=30, verbose_name="ظرفیت")
    homeroom_teacher = models.ForeignKey(
        "TeacherProfile", on_delete=models.SET_NULL, null=True, blank=True,
        related_name="homeroom_classes", verbose_name="معلم مسئول کلاس"
    )
    academic_year = models.CharField(max_length=20, default="1404-1405", verbose_name="سال تحصیلی")

    class Meta:
        verbose_name = "کلاس"
        verbose_name_plural = "کلاس‌ها"
        ordering = ["grade_level", "name"]

    def __str__(self):
        return self.name

    @property
    def student_count(self):
        return self.students.count()


class Subject(models.Model):
    name = models.CharField(max_length=100, verbose_name="نام درس")
    code = models.CharField(max_length=20, unique=True, verbose_name="کد درس")
    weekly_hours = models.PositiveSmallIntegerField(default=1, verbose_name="ساعت هفتگی")
    description = models.TextField(blank=True, verbose_name="توضیحات")

    class Meta:
        verbose_name = "درس"
        verbose_name_plural = "دروس"
        ordering = ["name"]

    def __str__(self):
        return self.name


class TeacherProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="teacher_profile")
    subjects = models.ManyToManyField(Subject, blank=True, related_name="teachers", verbose_name="دروس تدریسی")
    hire_date = models.DateField(null=True, blank=True, verbose_name="تاریخ استخدام")
    bio = models.TextField(blank=True, verbose_name="بیوگرافی")

    class Meta:
        verbose_name = "پروفایل معلم"
        verbose_name_plural = "پروفایل معلمان"

    def __str__(self):
        return self.user.get_full_name() or self.user.username


class StudentProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="student_profile")
    school_class = models.ForeignKey(
        SchoolClass, on_delete=models.SET_NULL, null=True, blank=True, related_name="students",
        verbose_name="کلاس"
    )
    student_number = models.CharField(max_length=20, unique=True, verbose_name="شماره دانش‌آموزی")
    birth_date = models.DateField(null=True, blank=True, verbose_name="تاریخ تولد")
    enrollment_date = models.DateField(auto_now_add=True, verbose_name="تاریخ ثبت‌نام")

    class Meta:
        verbose_name = "پروفایل دانش‌آموز"
        verbose_name_plural = "پروفایل دانش‌آموزان"

    def __str__(self):
        return self.user.get_full_name() or self.user.username


class ParentProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="parent_profile")
    children = models.ManyToManyField(StudentProfile, blank=True, related_name="parents", verbose_name="فرزندان")
    relation = models.CharField(max_length=30, default="پدر/مادر", verbose_name="نسبت")

    class Meta:
        verbose_name = "پروفایل والدین"
        verbose_name_plural = "پروفایل‌های والدین"

    def __str__(self):
        return self.user.get_full_name() or self.user.username


class TimetableEntry(models.Model):
    """برنامه هفتگی کلاس‌ها"""
    class Weekday(models.IntegerChoices):
        SATURDAY = 0, "شنبه"
        SUNDAY = 1, "یکشنبه"
        MONDAY = 2, "دوشنبه"
        TUESDAY = 3, "سه‌شنبه"
        WEDNESDAY = 4, "چهارشنبه"
        THURSDAY = 5, "پنجشنبه"

    school_class = models.ForeignKey(SchoolClass, on_delete=models.CASCADE, related_name="timetable_entries", verbose_name="کلاس")
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name="timetable_entries", verbose_name="درس")
    teacher = models.ForeignKey(TeacherProfile, on_delete=models.CASCADE, related_name="timetable_entries", verbose_name="معلم")
    weekday = models.IntegerField(choices=Weekday.choices, verbose_name="روز هفته")
    start_time = models.TimeField(verbose_name="ساعت شروع")
    end_time = models.TimeField(verbose_name="ساعت پایان")

    class Meta:
        verbose_name = "برنامه هفتگی"
        verbose_name_plural = "برنامه‌های هفتگی"
        ordering = ["weekday", "start_time"]
        unique_together = ("school_class", "weekday", "start_time")

    def __str__(self):
        return f"{self.school_class} - {self.subject} - {self.get_weekday_display()}"
