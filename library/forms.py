from django import forms
from .models import Book, Student, Pupil

class UserRegistrationForm(forms.Form):
    name = forms.CharField(max_length=100)
    surname = forms.CharField(max_length=100)
    group = forms.CharField(max_length=50)
    age = forms.IntegerField(min_value=1)

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name', 'surname', 'group']

class PupilForm(forms.ModelForm):
    class Meta:
        model = Pupil
        fields = ['name', 'surname', 'group', 'age']


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'isbn', 'year', 'quantity', 'label']