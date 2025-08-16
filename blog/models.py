from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from django.utils.text import slugify
from django.utils.html import format_html

# ==================================
# مدل دسته‌بندی (Category)
# ==================================- 
class Category(models.Model):
    """
    مدل برای دسته‌بندی مقالات.
    """
    title = models.CharField(max_length=100, verbose_name="عنوان دسته‌بندی")
    created = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")

    class Meta:
        verbose_name = "دسته‌بندی"
        verbose_name_plural = "دسته‌بندی‌ها"
        ordering = ['title'] # اضافه کردن مرتب‌سازی بر اساس عنوان

    def __str__(self):
        return self.title

# ==================================
# مدل مقاله (Article)
# ==================================
class Article(models.Model):
    """
    مدل اصلی برای مقالات وبلاگ.
    """
    # --- وضعیت مقاله ---
    # به جای دو فیلد Boolean، از یک فیلد CharField با گزینه‌های مشخص استفاده می‌کنیم.
    # این کار مدیریت وضعیت مقاله (پیش‌نویس، منتشر شده) را بسیار انعطاف‌پذیرتر می‌کند.
    STATUS_CHOICES = (
        ('d', 'پیش‌نویس'),      # Draft
        ('p', 'منتشر شده'),   # Published
    )
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='d', verbose_name="وضعیت انتشار")
    
    # --- روابط ---
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="articles", verbose_name="نویسنده")
    category = models.ManyToManyField(Category, related_name="articles", verbose_name="دسته‌بندی‌ها")
    
    # --- فیلدهای اصلی ---
    title = models.CharField(max_length=70, unique=True, verbose_name="عنوان مقاله")
    body = models.TextField(verbose_name="محتوای مقاله")
    image = models.ImageField(upload_to="articles/images/", blank=True, null=True, verbose_name="تصویر شاخص")
    slug = models.SlugField(blank=True, unique=True, allow_unicode=True, verbose_name="اسلاگ (آدرس)")

    # --- تاریخ‌ها ---
    created = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    updated = models.DateTimeField(auto_now=True, verbose_name="تاریخ بروزرسانی")
    
    class Meta:
        ordering = ("-created",)
        verbose_name = "مقاله"
        verbose_name_plural = "مقالات"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        """
        هنگام ذخیره، اگر اسلاگ وجود نداشت، آن را از روی عنوان بساز.
        """
        if not self.slug:
            self.slug = slugify(self.title, allow_unicode=True) # allow_unicode برای پشتیبانی از فارسی
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        """
        یک URL استاندارد برای هر مقاله برمی‌گرداند.
        """
        return reverse("blog:article_detail", kwargs={'slug': self.slug})
        
    def show_image(self):
        """
        متدی برای نمایش تصویر در پنل ادمین.
        """
        if self.image:
            return format_html(f'<img src="{self.image.url}" width="60px" height="50px" style="border-radius: 5px;">')
        return format_html('<span style="color:red;">بدون تصویر</span>')
    show_image.short_description = 'تصویر' # تغییر عنوان ستون در ادمین

# ==================================
# مدل نظرات (Comment)
# ==================================
class Comment(models.Model):
    """
    مدل برای ثبت نظرات کاربران برای هر مقاله.
    """
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments', verbose_name="مقاله")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_comments', verbose_name="کاربر")
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies', verbose_name="پاسخ به")
    
    body = models.TextField(verbose_name="متن نظر")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    is_active = models.BooleanField(default=True, verbose_name="فعال") # برای تایید یا عدم تایید کامنت توسط ادمین

    class Meta:
        ordering = ('-created_at',)
        verbose_name = "نظر"
        verbose_name_plural = "نظرات"

    def __str__(self):
        return f"نظر توسط {self.user.username} برای {self.article.title}"

# ==================================
# مدل لایک (Like)
# ==================================
class Like(models.Model):
    """
    مدل برای لایک کردن مقالات توسط کاربران.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_likes", verbose_name="کاربر")
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name="article_likes", verbose_name="مقاله")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "لایک"
        verbose_name_plural = "لایک‌ها"
        ordering = ('-created_at',)
        unique_together = ('user', 'article') # هر کاربر فقط یک بار می‌تواند یک مقاله را لایک کند

    def __str__(self):
        return f"{self.user.username} مقاله '{self.article.title}' را لایک کرده است"

# ==================================
# مدل پیام (Message)
# این مدل برای فرم "تماس با ما" مناسب است.
# ==================================
class Message(models.Model):
    """
    مدل برای پیام‌های کاربران از طریق فرم تماس با ما.
    """
    title = models.CharField(max_length=100, verbose_name="عنوان پیام")
    text = models.TextField(verbose_name="متن پیام")
    email = models.EmailField(verbose_name="ایمیل فرستنده")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ دریافت")

    class Meta:
        ordering = ('-created_at',)
        verbose_name = "پیام"
        verbose_name_plural = "پیام‌ها"

    def __str__(self):
        return self.title
