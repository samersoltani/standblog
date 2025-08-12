from django.contrib import admin
from .models import Category, Article, Comment, Like, Message

# ==================================
# مدیریت دسته‌بندی‌ها (Category)
# ==================================
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'created')
    search_fields = ('title',)

# ==================================
# نمایش نظرات به صورت Inline
# ==================================
class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0 # به طور پیش‌فرض فرم خالی برای نظر جدید نشان نده
    # این فیلدها فقط خواندنی هستند چون نظرات باید از بخش خودشان مدیریت شوند
    readonly_fields = ('user', 'body', 'created_at', 'parent', 'is_active')

# ==================================
# مدیریت مقالات (Article)
# ==================================
@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'status', 'created', 'show_image')
    list_filter = ('status', 'category', 'author')
    search_fields = ('title', 'body')
    prepopulated_fields = {'slug': ('title',)} 
    raw_id_fields = ('author',)
    filter_horizontal = ('category',)
    
    fieldsets = (
        ('اطلاعات اصلی', {
            'fields': ('title', 'slug', 'author', 'category', 'body', 'image')
        }),
        ('تنظیمات انتشار', {
            'fields': ('status',)
        }),
    )

    # --- راه‌حل مشکل ---
    # این متد به صورت هوشمند تصمیم می‌گیرد که فرم نظرات را نمایش بدهد یا نه
    def get_inlines(self, request, obj=None):
        """
        اگر در حال ویرایش یک مقاله موجود هستیم (obj وجود دارد)،
        فرم نظرات (CommentInline) را نمایش بده.
        در غیر این صورت (اگر در حال افزودن مقاله جدید هستیم)، آن را نمایش نده.
        """
        if obj:
            return (CommentInline,)
        else:
            return ()

# ==================================
# مدیریت نظرات (Comment)
# ==================================
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'article', 'created_at', 'is_active', 'parent')
    list_filter = ('is_active',)
    search_fields = ('user__username', 'article__title', 'body')
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(is_active=True)
    approve_comments.short_description = "تایید نظرات انتخاب شده"

# ==================================
# مدیریت پیام‌ها (Message)
# ==================================
@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('title', 'email', 'created_at')
    search_fields = ('title', 'email', 'text')
    readonly_fields = ('title', 'text', 'email', 'created_at')

# ==================================
# مدیریت لایک‌ها (Like)
# ==================================
@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'article', 'created_at')
    search_fields = ('user__username', 'article__title')
