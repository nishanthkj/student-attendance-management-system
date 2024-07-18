from django import forms
from .models import Student

class StudentForm(forms.ModelForm):
    studentImage = forms.ImageField(required=True)
    
    class Meta:
        model = Student
        fields = ['name', 'usn', 'studentImage']
