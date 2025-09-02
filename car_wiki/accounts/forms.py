import os
from django import forms
from .models import Comment, Profile, ModelSuggestion
from django.core.exceptions import ValidationError

# форма для комментария
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


# форма для обновления профиля (аватар)
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
        
def validate_image_file(value):
    ext = os.path.splitext(value.name)[1].lower()
    valid_extensions = ['.jpg', '.jpeg', '.png']
    if ext not in valid_extensions:
        raise ValidationError('Разрешены только файлы форматов: .jpg, .jpeg, .png')
    
class ModelSuggestionForm(forms.ModelForm):
    class Meta:
        model = ModelSuggestion
        fields = ['brand', 'model_name', 'year', 'description', 'image']
        widgets = {
            'brand': forms.Select(attrs={'class': 'form-control'}),
            'model_name': forms.TextInput(attrs={'class': 'form-control'}),
            'year': forms.NumberInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'image': 'Фото автомобиля (JPG или PNG)'
        }

    # Валидация поля image
    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            validate_image_file(image)
        return image
