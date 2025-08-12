# accounts/urls.py

from django.urls import path
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy # این خط را اضافه کن
from . import views

app_name = "accounts"

urlpatterns = [
    # ... مسیرهای دیگر شما
    path('login/', views.UserLoginView.as_view(), name="login"),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.user_register, name="register"),
    path('profile/edit/', views.user_edit, name="edit_profile"),
    
    # بخش تغییر رمز عبور
    path('password_change/', 
         auth_views.PasswordChangeView.as_view(
             template_name='accounts/password_change_form.html',
             success_url = reverse_lazy('accounts:password_change_done') # <-- تغییر اصلی اینجاست
         ), 
         name='password_change'),

    # بخش صفحه موفقیت تغییر رمز عبور
    path('password_change/done/', 
         auth_views.PasswordChangeDoneView.as_view( # <-- از ویوی آماده خود جنگو استفاده شد
             template_name='accounts/password_change_done.html'
         ), 
         name='password_change_done'),
    
    # ... مسیرهای بازیابی رمز عبور (بدون تغییر)
    path('password_reset/', 
         auth_views.PasswordResetView.as_view(
             template_name='accounts/password_reset_form.html',
             success_url=reverse_lazy('accounts:password_reset_done'), # بهتر است این هم اصلاح شود
             email_template_name='accounts/password_reset_email.html'
         ), 
         name='password_reset'),
    path('password_reset/done/', 
         auth_views.PasswordResetDoneView.as_view(
             template_name='accounts/password_reset_done.html'
         ), 
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/', 
         auth_views.PasswordResetConfirmView.as_view(
             template_name='accounts/password_reset_confirm.html',
             success_url=reverse_lazy('accounts:password_reset_complete') # بهتر است این هم اصلاح شود
         ), 
         name='password_reset_confirm'),
    path('reset/done/', 
         auth_views.PasswordResetCompleteView.as_view(
             template_name='accounts/password_reset_complete.html'
         ), 
         name='password_reset_complete'),
]