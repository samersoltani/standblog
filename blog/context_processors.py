from .models import Article, Category
from django.db.models import Count

def sidebar_data(request):
    """
    این تابع داده‌هایی که در سایدبار تمام صفحات لازم است را فراهم می‌کند.
    """
    
    # دریافت 5 مقاله آخر که "منتشر شده" هستند
    recent_posts = Article.objects.filter(status='p').order_by('-created')[:5]
    
    # دریافت تمام دسته‌بندی‌ها همراه با تعداد مقالات هر کدام
    # annotate یک فیلد جدید (num_articles) به هر دسته‌بندی اضافه می‌کند
    all_categories = Category.objects.annotate(num_articles=Count('articles')).filter(articles__status='p').distinct()

    # برگرداندن داده‌ها در قالب یک دیکشنری
    # کلیدهای این دیکشنری به عنوان متغیر در تمام تمپلیت‌ها در دسترس خواهند بود.
    return {
        'recent_posts': recent_posts,
        'all_categories': all_categories,
    }


def all_categories(request):
   # این کد با یک کوئری تمام دسته‌بندی‌هایی که حداقل یک مقاله دارند را پیدا می‌کند
    categories = Category.objects.annotate(num_articles=Count('articles')).filter(num_articles__gt=0)
    return {'all_categories': categories}