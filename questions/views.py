from django.shortcuts import get_object_or_404, redirect
from django.http import JsonResponse
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.db.models import F
from django.db import transaction

from .models import Question, Choice, Answer, Comment
from .forms import QuestionForm, ChoiceFormSet
from .models import Question
from .forms import QuestionForm, AnswerForm, CommentForm


class QuestionListView(ListView):
    model = Question
    template_name = 'questions/question_list.html'
    context_object_name = 'questions'
    ordering = ['-created_at']


class QuestionDetailView(DetailView):
    model = Question
    template_name = 'questions/question_detail.html'
    context_object_name = 'question'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Check if this question is liked in this session
        liked_questions = self.request.session.get('liked_questions', [])
        context['is_liked'] = self.object.pk in liked_questions
        
        # Add answers, comments and forms
        context['answers'] = self.object.answers.all().order_by('-votes', '-created_at')
        context['comments'] = self.object.comments.all().order_by('created_at')
        context['answer_form'] = AnswerForm()
        context['comment_form'] = CommentForm()
        return context

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        # Race-condition-safe view increment
        Question.objects.filter(pk=obj.pk).update(views=F('views') + 1)
        obj.refresh_from_db(fields=['views'])
        return obj


class QuestionCreateView(CreateView):
    model = Question
    form_class = QuestionForm
    template_name = 'questions/question_form.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        if self.request.POST:
            ctx['choices'] = ChoiceFormSet(self.request.POST)
        else:
            ctx['choices'] = ChoiceFormSet()
        ctx['form_title'] = 'Ask a New Question'
        ctx['submit_label'] = 'Create Question'
        return ctx

    def form_valid(self, form):
        context = self.get_context_data()
        choices = context['choices']
        with transaction.atomic():
            self.object = form.save()
            if choices.is_valid():
                choices.instance = self.object
                choices.save()
            
            # Handle True/False auto-population if it's empty
            if self.object.question_type == 'true_false' and not self.object.choices.exists():
                Choice.objects.create(question=self.object, text='True', is_correct=False)
                Choice.objects.create(question=self.object, text='False', is_correct=False)
                
        return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse('questions:detail', kwargs={'pk': self.object.pk})


class QuestionUpdateView(UpdateView):
    model = Question
    form_class = QuestionForm
    template_name = 'questions/question_form.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        if self.request.POST:
            ctx['choices'] = ChoiceFormSet(self.request.POST, instance=self.object)
        else:
            ctx['choices'] = ChoiceFormSet(instance=self.object)
        ctx['form_title'] = 'Edit Question'
        ctx['submit_label'] = 'Save Changes'
        return ctx

    def form_valid(self, form):
        context = self.get_context_data()
        choices = context['choices']
        with transaction.atomic():
            self.object = form.save()
            if choices.is_valid():
                choices.instance = self.object
                choices.save()
        return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse('questions:detail', kwargs={'pk': self.object.pk})


class QuestionDeleteView(DeleteView):
    model = Question
    template_name = 'questions/question_confirm_delete.html'
    context_object_name = 'question'
    success_url = reverse_lazy('questions:list')


def like_question(request, pk):
    """Toggle likes counter using sessions (POST only)."""
    if request.method == 'POST':
        liked_questions = request.session.get('liked_questions', [])
        
        if pk in liked_questions:
            # Unlike: decrement and remove from session
            Question.objects.filter(pk=pk).update(likes=F('likes') - 1)
            liked_questions.remove(pk)
        else:
            # Like: increment and add to session
            Question.objects.filter(pk=pk).update(likes=F('likes') + 1)
            liked_questions.append(pk)
        
        request.session['liked_questions'] = liked_questions
        request.session.modified = True
        
    return redirect(reverse('questions:detail', kwargs={'pk': pk}))


def create_answer(request, pk):
    """Handle answer submission for a specific question."""
    question = get_object_or_404(Question, pk=pk)
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.question = question
            answer.save()
    return redirect(reverse('questions:detail', kwargs={'pk': pk}))


def create_comment(request, pk):
    """Handle comment submission for a specific question."""
    question = get_object_or_404(Question, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.question = question
            comment.save()
    return redirect(reverse('questions:detail', kwargs={'pk': pk}))


def upvote_answer(request, pk):
    """Increment answer upvotes via AJAX."""
    if request.method == 'POST':
        Answer.objects.filter(pk=pk).update(
            upvotes=F('upvotes') + 1,
            votes=F('votes') + 1
        )
        answer = get_object_or_404(Answer, pk=pk)
        return JsonResponse({
            'votes': answer.votes,
            'upvotes': answer.upvotes,
            'downvotes': answer.downvotes
        })
    return JsonResponse({'error': 'Invalid request'}, status=400)


def downvote_answer(request, pk):
    """Increment answer downvotes via AJAX."""
    if request.method == 'POST':
        Answer.objects.filter(pk=pk).update(
            downvotes=F('downvotes') + 1,
            votes=F('votes') - 1
        )
        answer = get_object_or_404(Answer, pk=pk)
        return JsonResponse({
            'votes': answer.votes,
            'upvotes': answer.upvotes,
            'downvotes': answer.downvotes
        })
    return JsonResponse({'error': 'Invalid request'}, status=400)


class AnswerUpdateView(UpdateView):
    model = Answer
    form_class = AnswerForm
    template_name = 'questions/answer_form.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['form_title'] = 'Edit Answer'
        ctx['submit_label'] = 'Save Changes'
        return ctx

    def get_success_url(self):
        return reverse('questions:detail', kwargs={'pk': self.object.question.pk})


class AnswerDeleteView(DeleteView):
    model = Answer
    template_name = 'questions/answer_confirm_delete.html'
    context_object_name = 'answer'

    def get_success_url(self):
        return reverse('questions:detail', kwargs={'pk': self.object.question.pk})
