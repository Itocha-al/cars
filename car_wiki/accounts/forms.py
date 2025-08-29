from django import forms
from .models import Comment
from .models import Profile

# Форма для комментария
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Напишите ваш комментарий...',
                'class': 'form-control'
            })
        }
        labels = {'content': ''}


# Форма для обновления профиля (аватар)
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar']
        widgets = {
            'avatar': forms.ClearableFileInput(attrs={'class': 'form-control'})
        }
        labels = {
            'avatar': 'Аватар (PNG/JPG)'
        }
