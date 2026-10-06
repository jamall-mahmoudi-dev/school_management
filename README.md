# inii سامانه مدیریت دبیرستان (Django)

سیستم مدیریت یکپارچه دبیرستان با ۵ نقش کاربری: -ادمین-، -مدیر مدرسه-، -معلم-، -دانش‌آموز- و -والدین-.

## امکانات
- مدیریت کاربران (افزودن/ویرایش/حذف) به تفکیک نقش
- مدیریت کلاس‌ها، دروس و برنامه هفتگی
- ثبت و مشاهده حضور و غیاب (توسط معلم/مدیر — مشاهده توسط دانش‌آموز/والدین)
- کارنامه هفتگی / ماهانه
- ثبت نمرات و مشاهده کارنامه
- اطلاعیه‌های عمومی/هدفمند بر اساس نقش یا کلاس + پیام مستقیم بین کاربران
- داشبورد اختصاصی برای هر نقش با آمار و دسترسی سریع
- پنل مدیریت Django (admin) فارسی‌سازی‌شده
- طراحی واکنش‌گرا (Bootstrap 5 RTL) با فونت Vazirmatn

## نصب و راه‌اندازی

bash
# ۱. ساخت محیط مجازی
python -m venv venv
source venv/bin/activate      # ویندوز: venv\Scripts\activate

# ۲. نصب پکیج‌ها
pip install -r requirements.txt

# ۳. اجرای مایگریشن‌ها
python manage.py migrate

# ۴. (اختیاری ولی پیشنهادی) ساخت داده‌های نمونه برای تست
python manage.py seed_demo

# یا به‌جای مرحله ۴، یک ادمین دلخواه بسازید:
python manage.py createsuperuser

# ۵. اجرای سرور
python manage.py runserver


سپس آدرس http://127.0.0.1:8000 را باز کنید.
https://daneshpooyan.ir
http://daneshpooyan.ir
## کاربران نمونه (پس از اجرای seed_demo)

- نقش - نام کاربری - رمز عبور -
-------------------------------------------
- ادمین - admin - admin12345 -
- مدیر مدرسه - manager1 - pass12345 -
- معلم - teacher1 - pass12345 -
- دانش‌آموز - student1 (یا 2, 3) - pass12345 -
- والدین - parent1 - pass12345 -

پنل مدیریت Django: /admin/

## ساختار پروژه


config/            تنظیمات اصلی پروژه و URLها
accounts/          مدل کاربر سفارشی + مدیریت کاربران و ورود/خروج
academics/         کلاس‌ها، دروس، پروفایل معلم/دانش‌آموز/والدین، برنامه هفتگی
attendance/        حضور و غیاب
grades/            نمرات و کارنامه
notifications/     اطلاعیه‌ها و پیام مستقیم
core/               داشبورد، دسترسی نقش‌محور (mixins)، فرم پایه Bootstrap
templates/          تمام قالب‌های HTML
static/             CSS سفارشی


## نکات فنی
- مدل کاربر سفارشی (accounts.User) با فیلد role — نقش‌ها: ADMIN, MANAGER, TEACHER, STUDENT, PARENT
- کنترل دسترسی از طریق core.mixins.RoleRequiredMixin روی تمام ویوهای مدیریتی
- پایگاه داده پیش‌فرض SQLite (برای Production توصیه می‌شود PostgreSQL جایگزین شود)
- قبل از استفاده در Production حتماً DEBUG = False، SECRET_KEY جدید و ALLOWED_HOSTS مناسب تنظیم کنید (در config/settings.py)
