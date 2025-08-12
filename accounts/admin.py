from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from .models import Profile

# ==================================
# نمایش پروفایل به صورت Inline در صفحه کاربر
# ==================================
class ProfileInline(admin.StackedInline):
    """
    این کلاس به ما اجازه می‌دهد که مدل Profile را
    مستقیماً در صفحه ویرایش مدل User نمایش دهیم.
    """
    model = Profile
    can_delete = False # اجازه نمی‌دهیم پروفایل از اینجا حذف شود
    verbose_name_plural = 'پروفایل کاربر'
    # اگر فیلدهای زیادی دارید، می‌توانید آن‌ها را گروه‌بندی کنید
    # fieldsets = (('اطلاعات تکمیلی', {'fields': ('fathers_name', 'mli_code', 'image')}),)


# ==================================
# تعریف یک کلاس ادمین سفارشی برای مدل User
# ==================================
class UserAdmin(BaseUserAdmin):
    """
    این کلاس، کلاس ادمین پیش‌فرض User را با اضافه کردن
    بخش پروفایل (ProfileInline) گسترش می‌دهد.
    """
    inlines = (ProfileInline,)

# ==================================
# ثبت نهایی مدل‌ها
# ==================================

# ابتدا، ثبت پیش‌فرض مدل User را لغو می‌کنیم
admin.site.unregister(User)

# سپس، مدل User را با کلاس ادمین سفارشی خودمان دوباره ثبت می‌کنیم
admin.site.register(User, UserAdmin)

# شما همچنان می‌توانید مدل Profile را به صورت جداگانه هم ثبت کنید
# اگر می‌خواهید لیست تمام پروفایل‌ها را یکجا ببینید.
# @admin.register(Profile)
# class ProfileAdmin(admin.ModelAdmin):
#     list_display = ('user', 'mli_code')


# شخصی‌سازی عنوان و هدر پنل ادمین (کد شما عالی بود)
admin.site.site_header = 'مدیریت وبلاگ استند'
admin.site.site_title = 'پنل مدیریت'
admin.site.index_title = "به پنل مدیریت خوش آمدید"
