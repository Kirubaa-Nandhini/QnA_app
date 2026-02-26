from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.db.models import F

from .models import Question
from .forms import QuestionForm


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
        ctx['form_title'] = 'Ask a New Question'
        ctx['submit_label'] = 'Create Question'
        return ctx

    def get_success_url(self):
        return reverse('questions:detail', kwargs={'pk': self.object.pk})


class QuestionUpdateView(UpdateView):
    model = Question
    form_class = QuestionForm
    template_name = 'questions/question_form.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['form_title'] = 'Edit Question'
        ctx['submit_label'] = 'Save Changes'
        return ctx

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
