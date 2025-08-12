from django import forms
from .models import Comment, Message

class CommentForm(forms.ModelForm):
    """
    فرم برای ثبت نظر.
    ما فقط فیلد 'body' را به کاربر نمایش می‌دهیم و بقیه فیلدها
    (user, article, parent) را به صورت خودکار در ویو پر می‌کنیم.
    """
    class Meta:
        model = Comment
        fields = ('body',) # فقط این فیلد در فرم وجود دارد
        widgets = {
            'body': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'نظر خود را اینجا بنویسید...'
            }),
        }
        # برای اینکه برچسب (label) بالای فیلد نمایش داده نشود
        labels = {
            'body': '',
        }


class MessageForm(forms.ModelForm):
    """
    فرم برای صفحه "تماس با ما".
    """
    class Meta:
        model = Message
        fields = ('title', 'text', 'email')
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'عنوان پیام'}),
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 6, 'placeholder': 'متن پیام شما'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'ایمیل شما'}),
        }
