from django import forms
from .models import Lab9Book  # التغيير هنا

class BookForm(forms.ModelForm):
    class Meta:
        model = Lab9Book      # والتغيير هنا
        fields = ['title', 'price', 'quantity', 'pubdate', 'rating', 'publisher', 'authors']
        widgets = {
            'pubdate': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }