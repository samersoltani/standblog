from django.shortcuts import render
from blog.models import Article

def home(request):
    """
    ویو برای نمایش صفحه اصلی سایت.
    """
    
    # دریافت تمام مقالات "منتشر شده" به ترتیب از جدید به قدیم
    published_articles = Article.objects.filter(status='p').order_by('-created')

    # --- راه‌حل اصلی اینجاست ---
    # یک لیست جداگانه فقط از مقالات منتشر شده‌ای که "عکس دارند" برای بنر آماده می‌کنیم.
    # exclude(image__isnull=True) یعنی آنهایی که فیلد عکسشان خالی است را حذف کن.
    banner_articles = published_articles.exclude(image__isnull=True).exclude(image__exact='')[:6]
    
    context = {
        'all_articles': published_articles, # تمام مقالات برای بخش پایینی صفحه
        'banner_articles': banner_articles, # مقالات عکس‌دار برای اسلایدر بالا
    }
    
    return render(request, "home/index.html", context)

