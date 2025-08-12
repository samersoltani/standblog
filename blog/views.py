# ==================================
# وارد کردن ماژول‌ها و کتابخانه‌های لازم
# ==================================
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

# وارد کردن مدل‌ها و فرم‌های اپلیکیشن فعلی
from .models import Article, Category, Comment, Message, Like
from .forms import CommentForm, MessageForm




class ArticleListView(ListView):
    """
    نمایش لیست مقالات منتشر شده همراه با صفحه‌بندی (Pagination).
    این ویو جایگزین ویو تابعی articles_list می‌شود.
    """
    # 1. مشخص کردن مدل: به جنگو می‌گوییم داده‌ها را از کدام مدل بخواند.
    model = Article
    
    # 2. تعیین تمپلیت: مشخص می‌کند کدام فایل HTML برای نمایش این صفحه استفاده شود.
    template_name = 'blog/articles_list.html'
    
    # 3. نام متغیر در تمپلیت: در فایل HTML، لیست مقالات با نام `articles` در دسترس خواهد بود.
    context_object_name = 'articles'
    
    # 4. صفحه‌بندی: مشخص می‌کند در هر صفحه چند مقاله نمایش داده شود.
    paginate_by = 3

    def get_queryset(self):
        """
        این متد کوئری پیش‌فرض را بازنویسی می‌کند تا فقط مقالات "منتشر شده" را برگرداند.
        این یک فیلتر امنیتی و منطقی بسیار مهم است.
        """
        # مقالات را بر اساس وضعیت 'p' (Published) فیلتر کن
        return Article.objects.filter(status='p')


class ArticleDetailView(DetailView):
    """
    نمایش جزئیات کامل یک مقاله، نظرات آن و فرم ارسال نظر.
    این ویو جایگزین ویو تابعی article_detail می‌شود.
    """
    # 1. مشخص کردن مدل
    model = Article
    
    # 2. تعیین تمپلیت
    template_name = 'blog/article_details.html'
    
    # 3. نام متغیر در تمپلیت
    context_object_name = 'article'

    def get_queryset(self):
        """
        اطمینان حاصل می‌کند که فقط مقالات "منتشر شده" قابل مشاهده هستند.
        """
        return Article.objects.filter(status='p')

    def get_context_data(self, **kwargs):
        """
        این متد برای ارسال اطلاعات اضافی (علاوه بر خود مقاله) به تمپلیت استفاده می‌شود.
        """
        # 1. ابتدا متد اصلی را فراخوانی کن تا context پیش‌فرض (شامل مقاله) را بگیریم.
        context = super().get_context_data(**kwargs)
        
        # 2. فرم ارسال نظر را به context اضافه کن.
        context['comment_form'] = CommentForm()
        
        # 3. بررسی کن که آیا کاربر فعلی این مقاله را لایک کرده است یا نه.
        # این بخش برای نمایش دکمه "لایک شده" یا "لایک نشده" در تمپلیت کاربرد دارد.
        if self.request.user.is_authenticated:
            # اگر کاربر لاگین کرده بود، بررسی کن آیا لایکی از این کاربر برای این مقاله وجود دارد.
            context['is_liked'] = Like.objects.filter(article=self.object, user=self.request.user).exists()
        else:
            # اگر کاربر لاگین نکرده، مقدار is_liked را False قرار بده.
            context['is_liked'] = False
            
        # 4. تعداد کل لایک‌های مقاله را به context اضافه کن.
        context['total_likes'] = self.object.article_likes.count() # از related_name که در مدل تعریف کردیم استفاده می‌کنیم
        
        # 5. در نهایت context کامل شده را برگردان.
        return context


class CategoryArticleListView(ListView):
    """
    نمایش لیست مقالات مربوط به یک دسته‌بندی خاص.
    این ویو جایگزین ویو تابعی category_detail می‌شود.
    """
    model = Article
    template_name = 'blog/articles_list.html'
    context_object_name = 'articles'
    paginate_by = 3

    def get_queryset(self):
        """
        این متد مقالات را بر اساس دسته‌بندی که از URL گرفته شده، فیلتر می‌کند.
        """
        # 1. ابتدا دسته‌بندی مورد نظر را با استفاده از `pk` که از URL می‌آید، پیدا کن.
        self.category = get_object_or_404(Category, pk=self.kwargs['pk'])
        
        # 2. مقالات مربوط به این دسته‌بندی که "منتشر شده" هستند را برگردان.
        return Article.objects.filter(category=self.category, status='p')

    def get_context_data(self, **kwargs):
        """
        نام دسته‌بندی را هم به تمپلیت ارسال می‌کند تا در عنوان صفحه نمایش داده شود.
        """
        context = super().get_context_data(**kwargs)
        context['category'] = self.category # نام دسته‌بندی را به context اضافه کن
        return context


class SearchListView(ListView):
    """
    نمایش نتایج جستجو.
    این ویو جایگزین ویو تابعی search می‌شود.
    """
    model = Article
    template_name = 'blog/articles_list.html'
    context_object_name = 'articles'
    paginate_by = 3

    def get_queryset(self):
        """
        مقالات را بر اساس عبارت جستجو شده (q) فیلتر می‌کند.
        """
        # 1. عبارت جستجو را از پارامتر `q` در URL بخوان.
        query = self.request.GET.get('q')
        if query:
            # 2. اگر عبارتی برای جستجو وجود داشت، مقالاتی که عنوانشان شامل آن عبارت است را برگردان.
            # `__icontains` باعث می‌شود جستجو به حروف بزرگ و کوچک حساس نباشد.
            return Article.objects.filter(title__icontains=query, status='p')
        # 3. اگر عبارتی برای جستجو نبود، لیست خالی برگردان.
        return Article.objects.none()

    def get_context_data(self, **kwargs):
        """
        عبارت جستجو شده را به تمپلیت ارسال می‌کند تا در صفحه نمایش داده شود.
        """
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('q', '')
        return context


class ContactView(CreateView):
    """
    صفحه "تماس با ما" که از یک فرم برای ایجاد یک پیام جدید استفاده می‌کند.
    این ویو جایگزین ویوهای contact_us و MessageView می‌شود.
    """
    model = Message
    form_class = MessageForm
    template_name = 'blog/contact_us.html'
    # پس از ارسال موفق فرم، کاربر به همین صفحه (که حالا خالی است) هدایت می‌شود.
    success_url = reverse_lazy('blog:contact_us') 

    def form_valid(self, form):
        """
        این متد زمانی اجرا می‌شود که فرم معتبر باشد.
        """
        # در اینجا می‌توان کارهای اضافی مثل ارسال ایمیل به مدیر را انجام داد.
        # فعلا فقط پیام را ذخیره می‌کنیم.
        return super().form_valid(form)


# ===================================================================
# بخش نماهای تابعی (Function-Based Views - FBVs)
# این ویوها برای کارهای ساده و تک منظوره مثل ارسال نظر یا لایک کردن مناسب هستند.
# ===================================================================


@login_required
def add_comment(request, slug):
    """
    این ویو مسئول پردازش فرم ارسال نظر و پاسخ به نظرات است.
    """
    article = get_object_or_404(Article, slug=slug, status='p')
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.article = article
            new_comment.user = request.user
            
            # --- راه‌حل اصلی برای پاسخ به کامنت ---
            parent_id = request.POST.get('parent_id')
            if parent_id:
                try:
                    # کامنت والد را پیدا کرده و به کامنت جدید اختصاص بده
                    parent_comment = Comment.objects.get(id=parent_id)
                    new_comment.parent = parent_comment
                except Comment.DoesNotExist:
                    # اگر کامنت والد پیدا نشد، مشکلی نیست. به صورت نظر اصلی ثبت می‌شود.
                    pass
            # --- پایان راه‌حل ---
            
            new_comment.save()
            # کاربر را به همان صفحه مقاله و بخش نظرات هدایت کن
            return redirect(article.get_absolute_url() + '#comments-section')
            
    # اگر متد GET بود یا فرم نامعتبر بود، به صفحه مقاله برگردان
    return redirect('blog:article_detail', slug=article.slug)


@login_required # فقط کاربران لاگین کرده می‌توانند لایک کنند.
def like_article(request, slug):
    """
    این ویو مسئول لایک کردن یا برداشتن لایک از یک مقاله است.
    """
    # 1. مقاله مورد نظر را پیدا کن.
    article = get_object_or_404(Article, slug=slug, status='p')
    
    # 2. با استفاده از `get_or_create` سعی کن یک لایک برای این کاربر و این مقاله پیدا کنی یا بسازی.
    # این متد یک تاپل برمی‌گرداند: (شیء لایک, یک مقدار Boolean به نام created)
    # اگر لایک از قبل وجود داشته باشد، created برابر False خواهد بود.
    # اگر لایک در همین لحظه ساخته شود، created برابر True خواهد بود.
    like, created = Like.objects.get_or_create(article=article, user=request.user)

    # 3. اگر لایک از قبل وجود داشت (created is False)، یعنی کاربر می‌خواهد لایکش را بردارد.
    if not created:
        like.delete() # لایک را حذف کن.
    
    # 4. در هر صورت، کاربر را به صفحه جزئیات مقاله برگردان.
    return redirect('blog:article_detail', slug=slug)

