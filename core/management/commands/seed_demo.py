from datetime import date, time

from django.core.management.base import BaseCommand
from django.db import transaction

from accounts.models import User
from academics.models import SchoolClass, Subject, TeacherProfile, StudentProfile, ParentProfile, TimetableEntry
from attendance.models import Attendance
from grades.models import Grade
from notifications.models import Announcement


class Command(BaseCommand):
    help = "ایجاد داده‌های نمونه برای تست سامانه (کاربران، کلاس، دروس، نمرات و ...)"

    @transaction.atomic
    def handle(self, *args, **options):
        if not User.objects.filter(username="admin").exists():
            User.objects.create_superuser(
                "admin", "admin@example.com", "admin12345",
                role=User.Role.ADMIN, first_name="مدیر", last_name="سیستم",
            )
            self.stdout.write(self.style.SUCCESS("ادمین ساخته شد: admin / admin12345"))

        manager, _ = User.objects.get_or_create(
            username="manager1", defaults=dict(first_name="سارا", last_name="احمدی", role=User.Role.MANAGER)
        )
        manager.set_password("pass12345")
        manager.save()

        subj_math, _ = Subject.objects.get_or_create(name="ریاضی", code="MATH1", defaults={"weekly_hours": 4})
        subj_phys, _ = Subject.objects.get_or_create(name="فیزیک", code="PHYS1", defaults={"weekly_hours": 3})

        teacher_user, _ = User.objects.get_or_create(
            username="teacher1", defaults=dict(first_name="علی", last_name="رضایی", role=User.Role.TEACHER)
        )
        teacher_user.set_password("pass12345")
        teacher_user.save()
        teacher_profile, _ = TeacherProfile.objects.get_or_create(user=teacher_user, defaults={"hire_date": date(2020, 9, 1)})
        teacher_profile.subjects.set([subj_math, subj_phys])

        school_class, _ = SchoolClass.objects.get_or_create(
            name="دهم ریاضی ۱", defaults={"grade_level": 10, "section": "1", "homeroom_teacher": teacher_profile}
        )

        TimetableEntry.objects.get_or_create(
            school_class=school_class, subject=subj_math, teacher=teacher_profile,
            weekday=0, start_time=time(8, 0), end_time=time(9, 0),
        )

        first_student_profile = None
        for i in range(1, 4):
            su, _ = User.objects.get_or_create(
                username=f"student{i}", defaults=dict(first_name=f"دانش‌آموز{i}", last_name="نمونه", role=User.Role.STUDENT)
            )
            su.set_password("pass12345")
            su.save()
            sp, _ = StudentProfile.objects.get_or_create(
                user=su, defaults={"student_number": f"100{i}", "school_class": school_class}
            )
            if i == 1:
                first_student_profile = sp
            Grade.objects.get_or_create(
                student=sp, subject=subj_math, teacher=teacher_profile, grade_type="QUIZ",
                term="FIRST", score=18.5, date=date(2026, 9, 10),
            )
            Attendance.objects.get_or_create(
                student=sp, school_class=school_class, date=date(2026, 9, 20),
                defaults={"status": "PRESENT", "recorded_by": teacher_user},
            )

        pu, _ = User.objects.get_or_create(
            username="parent1", defaults=dict(first_name="محمد", last_name="نمونه", role=User.Role.PARENT)
        )
        pu.set_password("pass12345")
        pu.save()
        pp, _ = ParentProfile.objects.get_or_create(user=pu, defaults={"relation": "پدر"})
        if first_student_profile:
            pp.children.add(first_student_profile)

        Announcement.objects.get_or_create(
            title="شروع سال تحصیلی", content="سال تحصیلی جدید از هفته آینده آغاز می‌شود.",
            audience="ALL", created_by=manager,
        )

        self.stdout.write(self.style.SUCCESS("داده‌های نمونه با موفقیت ساخته شد."))
        self.stdout.write("کاربران نمونه (رمز عبور همه: pass12345 | ادمین: admin12345):")
        self.stdout.write("  admin (ADMIN) / admin12345")
        self.stdout.write("  manager1 (MANAGER)")
        self.stdout.write("  teacher1 (TEACHER)")
        self.stdout.write("  student1, student2, student3 (STUDENT)")
        self.stdout.write("  parent1 (PARENT)")
