from django import forms
from .models import Review, Game


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'text']
        widgets = {
            'rating': forms.Select(attrs={'class': 'form-control', 'style': 'width: auto; display: inline-block; margin-left: 10px;'},choices=[(i, str(i)) for i in range(1, 6)]),
            'text': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Расскажите, что вам понравилось, а что нужно доработать...',
                'rows': 4,
                'style': 'width: 100%; border-radius: 8px; border: 1px solid #ddd; padding: 10px; resize: vertical;'
            }),
        }


class GameForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = ['title', 'description', 'category', 'status', 'cover_image', 'game_url']


