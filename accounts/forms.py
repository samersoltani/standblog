from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Profile # این خط را نگه می‌داریم برای فرم‌های دیگر

# ==================================
# فرم ثبت‌نام (ساخته شده از پایه)
# ==================================
class RegistrationForm(forms.Form):
    """
    این یک فرم ثبت‌نام کاملاً سفارشی است که هیچ وابستگی پنهانی ندارد.
    """
    username = forms.CharField(max_length=150, label="نام کاربری")
    email = forms.EmailField(label="ایمیل")
    password = forms.CharField(label="رمز عبور", widget=forms.PasswordInput)
    password2 = forms.CharField(label="تکرار رمز عبور", widget=forms.PasswordInput)

    def clean_username(self):
        """یک متد سفارشی برای اعتبارسنجی نام کاربری."""
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError("این نام کاربری قبلاً استفاده شده است.")
        return username

    def clean_email(self):
        """یک متد سفارشی برای اعتبارسنجی ایمیل."""
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("این ایمیل قبلاً ثبت شده است.")
        return email

    def clean(self):
        """یک متد کلی برای اعتبارسنجی کل فرم."""
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password2 = cleaned_data.get("password2")

        if password and password2 and password != password2:
            self.add_error('password2', "رمزهای عبور با هم تطابق ندارند.")
        
        return cleaned_data


# ==================================
# فرم‌های ویرایش (بدون تغییر)
# ==================================
class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'نام'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'نام خانوادگی'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'ایمیل'}),
        }

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('fathers_name', 'mli_code', 'image')
        widgets = {
            'fathers_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'نام پدر'}),
            'mli_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'کد ملی'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }
