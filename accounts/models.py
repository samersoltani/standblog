from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# ==================================
# مدل پروفایل کاربر
# ==================================
class Profile(models.Model):
    """
    این مدل، اطلاعات اضافی را به مدل User پیش‌فرض جنگو اضافه می‌کند.
    """
    # نکته: نام کلاس به Profile تغییر کرد (حرف اول بزرگ)
    
    # رابطه یک به یک: هر کاربر فقط یک پروفایل دارد.
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', verbose_name="کاربر")
    
    # فیلدهای اضافی
    fathers_name = models.CharField(max_length=50, verbose_name="نام پدر", blank=True)
    mli_code = models.CharField(max_length=10, verbose_name="کد ملی", blank=True)
    image = models.ImageField(upload_to="profiles/images", blank=True, null=True, verbose_name="تصویر پروفایل")

    class Meta:
        verbose_name = 'حساب کاربری'
        verbose_name_plural = 'حساب های کاربری' # نکته: فاصله اضافی حذف شد

    def __str__(self):
        return self.user.username

# ==================================
# بخش سیگنال‌ها (Signals)
# ==================================
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    این سیگنال به صورت خودکار اجرا می‌شود هر وقت یک شیء User ذخیره می‌شود.
    اگر کاربر 'جدید' باشد (created=True)، یک پروفایل برای او می‌سازد.
    """
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """
    این سیگنال تضمین می‌کند که هر وقت شیء User ذخیره شد،
    پروفایل مربوط به آن هم ذخیره شود.
    """
    instance.profile.save()
