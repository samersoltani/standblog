from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.views import LoginView, PasswordChangeDoneView
from django.contrib.auth.models import User # وارد کردن مدل User

# فرم‌های سفارشی خودمان را وارد می‌کنیم
from .forms import RegistrationForm, UserEditForm, ProfileEditForm

# ==================================
# ویوی ورود کاربر
# ==================================
class UserLoginView(LoginView):
    template_name = 'accounts/login.html'

# ==================================
# ویوی ثبت‌نام (با استفاده از فرم دستی و بدون باگ)
# ==================================
def user_register(request):
    if request.user.is_authenticated:
        return redirect('home_app:home')

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            # ما کاربر را به صورت دستی می‌سازیم تا از هرگونه باگ جلوگیری کنیم
            user = User.objects.create_user(
                username=form.cleaned_data.get('username'),
                email=form.cleaned_data.get('email'),
                password=form.cleaned_data.get('password')
            )
            messages.success(request, f'حساب کاربری برای {user.username} با موفقیت ساخته شد. اکنون می‌توانید وارد شوید.')
            return redirect('accounts:login')
    else:
        form = RegistrationForm()
        
    return render(request, 'accounts/register.html', {'form': form})

# ==================================
# ویوی ویرایش پروفایل
# ==================================
@login_required
def user_edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(request.POST, instance=request.user)
        profile_form = ProfileEditForm(request.POST, request.FILES, instance=request.user.profile)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'پروفایل شما با موفقیت به‌روزرسانی شد.')
            return redirect('accounts:edit_profile')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }
    return render(request, 'accounts/edit_profile.html', context)

# ==================================
# ویوی خروج کاربر
# ==================================
@login_required
def user_logout(request):
    logout(request)
    messages.info(request, 'شما با موفقیت از حساب کاربری خود خارج شدید.')
    return redirect('home_app:home')

# ==================================
# ویوی سفارشی برای نمایش پیام بعد از تغییر رمز
# ==================================
class CustomPasswordChangeDoneView(PasswordChangeDoneView):
    """
    این ویو سفارشی، یک پیام موفقیت‌آمیز به سیستم پیام‌رسانی جنگو اضافه می‌کند.
    """
    def dispatch(self, *args, **kwargs):
        messages.success(self.request, 'رمز عبور شما با موفقیت تغییر کرد.')
        return super().dispatch(*args, **kwargs)
