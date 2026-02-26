from django import forms
from .models import Question

_input_cls = 'w-full bg-gray-800 border border-gray-700 text-gray-100 rounded-lg px-4 py-2.5 focus:outline-none focus:ring-2 focus:ring-brand focus:border-transparent placeholder-gray-500 transition'
_select_cls = 'w-full bg-gray-800 border border-gray-700 text-gray-100 rounded-lg px-4 py-2.5 focus:outline-none focus:ring-2 focus:ring-brand focus:border-transparent transition'


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['text', 'question_type', 'difficulty', 'tags', 'choice1', 'choice2', 'choice3']
        widgets = {
            'text': forms.Textarea(attrs={'class': _input_cls, 'rows': 4, 'placeholder': 'Enter your question here...'}),
            'question_type': forms.Select(attrs={'class': _select_cls, 'id': 'id_question_type'}),
            'difficulty': forms.Select(attrs={'class': _select_cls}),
            'tags': forms.TextInput(attrs={'class': _input_cls, 'placeholder': 'e.g. math, algebra, quadratic'}),
            'choice1': forms.TextInput(attrs={'class': _input_cls, 'placeholder': 'Option 1'}),
            'choice2': forms.TextInput(attrs={'class': _input_cls, 'placeholder': 'Option 2'}),
            'choice3': forms.TextInput(attrs={'class': _input_cls, 'placeholder': 'Option 3'}),
        }
        labels = {
            'text': 'Question',
            'question_type': 'Type',
            'difficulty': 'Difficulty',
            'tags': 'Tags (comma-separated)',
            'choice1': 'Choice 1',
            'choice2': 'Choice 2',
            'choice3': 'Choice 3',
        }
