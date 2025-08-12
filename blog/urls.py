from django.urls import path, re_path
from . import views

app_name = 'blog'

urlpatterns = [
    # ==================================
    # مسیرهای اصلی و عمومی وبلاگ
    # ==================================
    
    path('articles/', views.ArticleListView.as_view(), name='articles_list'),

    # این خط اصلاح شد تا از اسلاگ فارسی پشتیبانی کند
    re_path(r'^article/(?P<slug>[^/]+)/$', views.ArticleDetailView.as_view(), name='article_detail'),

    path('category/<int:pk>/', views.CategoryArticleListView.as_view(), name='category_list'),
    path('search/', views.SearchListView.as_view(), name='search'),
    path('contact-us/', views.ContactView.as_view(), name='contact_us'),

    # ==================================
    # مسیرهای مربوط به تعاملات کاربر (Actions)
    # ==================================

    # این خط هم اصلاح شد تا از اسلاگ فارسی پشتیبانی کند
    re_path(r'^article/(?P<slug>[^/]+)/comment/$', views.add_comment, name='add_comment'),

    # این خط هم اصلاح شد تا از اسلاگ فارسی پشتیبانی کند
    re_path(r'^article/(?P<slug>[^/]+)/like/$', views.like_article, name='like_article'),
]