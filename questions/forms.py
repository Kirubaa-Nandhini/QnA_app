from django import forms
from .models import Question, Choice

_input_cls = 'w-full bg-gray-800 border border-gray-700 text-gray-100 rounded-lg px-4 py-2.5 focus:outline-none focus:ring-2 focus:ring-brand focus:border-transparent placeholder-gray-500 transition'
_select_cls = 'w-full bg-gray-800 border border-gray-700 text-gray-100 rounded-lg px-4 py-2.5 focus:outline-none focus:ring-2 focus:ring-brand focus:border-transparent transition'


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['text', 'question_type', 'difficulty', 'tags']
        widgets = {
            'text': forms.Textarea(attrs={'class': _input_cls, 'rows': 4, 'placeholder': 'Enter your question here...'}),
            'question_type': forms.Select(attrs={'class': _select_cls, 'id': 'id_question_type'}),
            'difficulty': forms.Select(attrs={'class': _select_cls}),
            'tags': forms.TextInput(attrs={'class': _input_cls, 'placeholder': 'e.g. math, algebra, quadratic'}),
        }
        labels = {
            'text': 'Question',
            'question_type': 'Type',
            'difficulty': 'Difficulty',
            'tags': 'Tags (comma-separated)',
        }


<<<<<<< HEAD
class ChoiceForm(forms.ModelForm):
    class Meta:
        model = Choice
        fields = ['text', 'is_correct']
        widgets = {
            'text': forms.TextInput(attrs={'class': _input_cls, 'placeholder': 'Choice text...'}),
            'is_correct': forms.CheckboxInput(attrs={'class': 'correct-answer-checkbox w-5 h-5 bg-gray-800 border-gray-700 rounded-full text-brand focus:ring-brand cursor-pointer'}),
        }


ChoiceFormSet = forms.inlineformset_factory(
    Question, Choice,
    form=ChoiceForm,
    extra=1,
    can_delete=True
)
=======
from .models import Answer, Comment

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={
                'class': _input_cls,
                'rows': 4,
                'placeholder': 'Write your answer here...'
            }),
        }
        labels = {
            'text': 'Your Answer',
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={
                'class': _input_cls,
                'rows': 3,
                'placeholder': 'Add a comment...'
            }),
        }
        labels = {
            'text': 'Comment',
        }
>>>>>>> 1c60386 (feat: implement Answer Management module with CRUD)
