from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone
from datetime import timedelta
from django.http import JsonResponse
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.db.models import F, Q, Count
from django.db import transaction
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

from .models import Question, Choice, Answer, Comment
from .forms import QuestionForm, ChoiceFormSet
from .models import Question
from .forms import QuestionForm, AnswerForm, CommentForm


class QuestionListView(ListView):
    model = Question
    template_name = 'questions/question_list.html'
    context_object_name = 'questions'
    ordering = ['-created_at']

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        date_filter = self.request.GET.get('date')
        unanswered = self.request.GET.get('unanswered')
        
        # Keyword Search
        if query:
            keywords = query.split()
            q_objects = Q()
            for word in keywords:
                q_objects &= (
                    Q(text__icontains=word) | 
                    Q(tags__icontains=word) | 
                    Q(author__username__icontains=word)
                )
            queryset = queryset.filter(q_objects)

        # Date Filtering
        if date_filter:
            now = timezone.now()
            if date_filter == 'today':
                queryset = queryset.filter(created_at__date=now.date())
            elif date_filter == 'week':
                queryset = queryset.filter(created_at__gte=now - timedelta(days=7))
            elif date_filter == 'month':
                queryset = queryset.filter(created_at__gte=now - timedelta(days=30))

        # Answer Status Filtering
        if unanswered == '1':
            queryset = queryset.annotate(answer_count=Count('answers')).filter(answer_count=0)
            
        return queryset

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        date_filter = self.request.GET.get('date', '')
        ctx['query'] = self.request.GET.get('q', '')
        ctx['current_date'] = date_filter
        ctx['is_today'] = date_filter == 'today'
        ctx['is_week'] = date_filter == 'week'
        ctx['is_month'] = date_filter == 'month'
        ctx['unanswered'] = self.request.GET.get('unanswered', '')
        return ctx


class QuestionDetailView(DetailView):
    model = Question
    template_name = 'questions/question_detail.html'
    context_object_name = 'question'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Check if this question is liked/voted in this session
        user = self.request.user
        context['is_liked'] = self.object.liked_by.filter(pk=user.pk).exists() if user.is_authenticated else False
        context['user_upvoted'] = self.object.upvoted_by.filter(pk=user.pk).exists() if user.is_authenticated else False
        context['user_downvoted'] = self.object.downvoted_by.filter(pk=user.pk).exists() if user.is_authenticated else False
        
        # pass answer vote status
        answers = self.object.answers.all().order_by('-votes', '-created_at')
        if user.is_authenticated:
            for answer in answers:
                answer.user_upvoted = answer.upvoted_by.filter(pk=user.pk).exists()
                answer.user_downvoted = answer.downvoted_by.filter(pk=user.pk).exists()
        context['answers'] = answers
        context['comments'] = self.object.comments.all().order_by('created_at')
        context['answer_form'] = AnswerForm()
        context['comment_form'] = CommentForm()

        # Related Questions Discovery
        tags = [t.strip() for t in self.object.tags.split(',') if t.strip()]
        if tags:
            # Match questions sharing any of the same tags, excluding current
            related_q_objects = Q()
            for tag in tags:
                related_q_objects |= Q(tags__icontains=tag)
                
            context['related_questions'] = Question.objects.filter(related_q_objects)\
                                                           .exclude(pk=self.object.pk)\
                                                           .distinct()[:5]
        else:
            context['related_questions'] = Question.objects.exclude(pk=self.object.pk).order_by('-views')[:5]

        return context

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        # Race-condition-safe view increment
        Question.objects.filter(pk=obj.pk).update(views=F('views') + 1)
        obj.refresh_from_db(fields=['views'])
        return obj


class QuestionCreateView(LoginRequiredMixin, CreateView):
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
            form.instance.author = self.request.user
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


class QuestionUpdateView(LoginRequiredMixin, UpdateView):
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


class QuestionDeleteView(LoginRequiredMixin, DeleteView):
    model = Question
    template_name = 'questions/question_confirm_delete.html'
    context_object_name = 'question'
    success_url = reverse_lazy('questions:list')


@login_required
def upvote_question(request, pk):
    """Toggle upvote for a question via AJAX."""
    if request.method == 'POST':
        question = get_object_or_404(Question, pk=pk)
        user = request.user
        
        with transaction.atomic():
            if question.upvoted_by.filter(pk=user.pk).exists():
                # Remove upvote
                question.upvoted_by.remove(user)
                question.upvotes = F('upvotes') - 1
                question.votes = F('votes') - 1
            else:
                # Add upvote (and remove downvote if present)
                if question.downvoted_by.filter(pk=user.pk).exists():
                    question.downvoted_by.remove(user)
                    question.downvotes = F('downvotes') - 1
                    question.votes = F('votes') + 1
                
                question.upvoted_by.add(user)
                question.upvotes = F('upvotes') + 1
                question.votes = F('votes') + 1
            
            question.save()
            question.refresh_from_db()
            
        return JsonResponse({
            'votes': question.votes,
            'upvotes': question.upvotes,
            'downvotes': question.downvotes,
            'user_upvoted': question.upvoted_by.filter(pk=user.pk).exists(),
            'user_downvoted': question.downvoted_by.filter(pk=user.pk).exists(),
        })
    return JsonResponse({'error': 'Invalid request'}, status=400)


@login_required
def downvote_question(request, pk):
    """Toggle downvote for a question via AJAX."""
    if request.method == 'POST':
        question = get_object_or_404(Question, pk=pk)
        user = request.user
        
        with transaction.atomic():
            if question.downvoted_by.filter(pk=user.pk).exists():
                # Remove downvote
                question.downvoted_by.remove(user)
                question.downvotes = F('downvotes') - 1
                question.votes = F('votes') + 1
            else:
                # Add downvote (and remove upvote if present)
                if question.upvoted_by.filter(pk=user.pk).exists():
                    question.upvoted_by.remove(user)
                    question.upvotes = F('upvotes') - 1
                    question.votes = F('votes') - 1
                
                question.downvoted_by.add(user)
                question.downvotes = F('downvotes') + 1
                question.votes = F('votes') - 1
            
            question.save()
            question.refresh_from_db()
            
        return JsonResponse({
            'votes': question.votes,
            'upvotes': question.upvotes,
            'downvotes': question.downvotes,
            'user_upvoted': question.upvoted_by.filter(pk=user.pk).exists(),
            'user_downvoted': question.downvoted_by.filter(pk=user.pk).exists(),
        })
    return JsonResponse({'error': 'Invalid request'}, status=400)


@login_required
def like_question(request, pk):
    """Toggle likes using Many-to-Many field."""
    if request.method == 'POST':
        question = get_object_or_404(Question, pk=pk)
        user = request.user
        
        if question.liked_by.filter(pk=user.pk).exists():
            question.liked_by.remove(user)
            Question.objects.filter(pk=pk).update(likes=F('likes') - 1)
        else:
            question.liked_by.add(user)
            Question.objects.filter(pk=pk).update(likes=F('likes') + 1)
            
    return redirect(reverse('questions:detail', kwargs={'pk': pk}))


@login_required
def create_answer(request, pk):
    """Handle answer submission for a specific question."""
    question = get_object_or_404(Question, pk=pk)
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.question = question
            answer.author = request.user
            answer.save()
    return redirect(reverse('questions:detail', kwargs={'pk': pk}))


@login_required
def create_comment(request, pk):
    """Handle comment submission for a specific question."""
    question = get_object_or_404(Question, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.question = question
            comment.author = request.user
            comment.save()
    return redirect(reverse('questions:detail', kwargs={'pk': pk}))


@login_required
def upvote_answer(request, pk):
    """Toggle upvote for an answer via AJAX."""
    if request.method == 'POST':
        answer = get_object_or_404(Answer, pk=pk)
        user = request.user
        
        with transaction.atomic():
            if answer.upvoted_by.filter(pk=user.pk).exists():
                # Remove upvote
                answer.upvoted_by.remove(user)
                answer.upvotes = F('upvotes') - 1
                answer.votes = F('votes') - 1
            else:
                # Add upvote (and remove downvote if present)
                if answer.downvoted_by.filter(pk=user.pk).exists():
                    answer.downvoted_by.remove(user)
                    answer.downvotes = F('downvotes') - 1
                    answer.votes = F('votes') + 1 # Neutralize the -1 from downvote
                
                answer.upvoted_by.add(user)
                answer.upvotes = F('upvotes') + 1
                answer.votes = F('votes') + 1
            
            answer.save()
            answer.refresh_from_db()
            
        return JsonResponse({
            'votes': answer.votes,
            'upvotes': answer.upvotes,
            'downvotes': answer.downvotes,
            'user_upvoted': answer.upvoted_by.filter(pk=user.pk).exists(),
            'user_downvoted': answer.downvoted_by.filter(pk=user.pk).exists(),
        })
    return JsonResponse({'error': 'Invalid request'}, status=400)


@login_required
def downvote_answer(request, pk):
    """Toggle downvote for an answer via AJAX."""
    if request.method == 'POST':
        answer = get_object_or_404(Answer, pk=pk)
        user = request.user
        
        with transaction.atomic():
            if answer.downvoted_by.filter(pk=user.pk).exists():
                # Remove downvote
                answer.downvoted_by.remove(user)
                answer.downvotes = F('downvotes') - 1
                answer.votes = F('votes') + 1
            else:
                # Add downvote (and remove upvote if present)
                if answer.upvoted_by.filter(pk=user.pk).exists():
                    answer.upvoted_by.remove(user)
                    answer.upvotes = F('upvotes') - 1
                    answer.votes = F('votes') - 1 # Neutralize the +1 from upvote
                
                answer.downvoted_by.add(user)
                answer.downvotes = F('downvotes') + 1
                answer.votes = F('votes') - 1
            
            answer.save()
            answer.refresh_from_db()
            
        return JsonResponse({
            'votes': answer.votes,
            'upvotes': answer.upvotes,
            'downvotes': answer.downvotes,
            'user_upvoted': answer.upvoted_by.filter(pk=user.pk).exists(),
            'user_downvoted': answer.downvoted_by.filter(pk=user.pk).exists(),
        })
    return JsonResponse({'error': 'Invalid request'}, status=400)


class AnswerUpdateView(LoginRequiredMixin, UpdateView):
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


class AnswerDeleteView(LoginRequiredMixin, DeleteView):
    model = Answer
    template_name = 'questions/answer_confirm_delete.html'
    context_object_name = 'answer'

    def get_success_url(self):
        return reverse('questions:detail', kwargs={'pk': self.object.question.pk})
