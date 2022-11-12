from django import forms

from .models import Topic, Entry

class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['text']
        labels = {'text': ''}
        widgets = {
            "text": forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Topic name',
                'id': "floatingInput",
            })
        }

class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ('text', 'image')
        labels = {'text': '', 'image': ''}
        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'form-control mb-3',
                'placeholder': 'Fill a new entry',
                'cols': 80
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control',
                'type': 'file',
                'id': 'formFile',
            }),
        }