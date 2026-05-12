from django import forms
from .models import Lab9Book 
from .models import Student 
from .models import Student2
from .models import StudentImage

class ImageForm(forms.ModelForm):
    class Meta:
        model = StudentImage
        fields = '__all__'

class BookForm(forms.ModelForm):
    class Meta:
        model = Lab9Book       
        fields = ['title', 'price', 'quantity', 'pubdate', 'rating', 'publisher', 'authors']
        widgets = {
            'pubdate': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name', 'age', 'address'] 
        
    widgets = {
        'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'اسم الطالب'}),
        'age': forms.NumberInput(attrs={'class': 'form-control'}),
        'address': forms.Select(attrs={'class': 'form-control'}),
    }


class Student2Form(forms.ModelForm):
    class Meta:
        model = Student2
        fields = '__all__'