from django.db import models
from django.contrib.auth.models import User


class Question(models.Model):
    QUESTION_TYPE_CHOICES = [
        ('multiple_choice', 'Multiple Choice'),
        ('true_false', 'True / False'),
        ('short_answer', 'Short Answer'),
    ]

    DIFFICULTY_CHOICES = [
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    ]

    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='questions')
    text = models.TextField(verbose_name='Question Text')
    question_type = models.CharField(
        max_length=20,
        choices=QUESTION_TYPE_CHOICES,
        verbose_name='Question Type',
    )
    difficulty = models.CharField(
        max_length=10,
        choices=DIFFICULTY_CHOICES,
        verbose_name='Difficulty',
    )
    tags = models.CharField(
        max_length=255,
        blank=True,
        default='',
        verbose_name='Tags',
        help_text='Comma-separated keywords, e.g. math, algebra',
    )
    correct_answer = models.TextField(
        blank=True,
        null=True,
        verbose_name='Correct Answer',
        help_text='Only for Short Answer type questions'
    )
    views = models.PositiveIntegerField(default=0, verbose_name='Views')
    likes = models.PositiveIntegerField(default=0, verbose_name='Likes')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Question'
        verbose_name_plural = 'Questions'

    def __str__(self):
        return self.text[:80]

    def tag_list(self):
        """Return tags as a cleaned list."""
        return [t.strip() for t in self.tags.split(',') if t.strip()]


class Choice(models.Model):
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name='choices',
        verbose_name='Question'
    )
    text = models.CharField(max_length=255, verbose_name='Choice Text')
    is_correct = models.BooleanField(default=False, verbose_name='Is Correct?')

    def __str__(self):
        return f"{self.question.text[:20]} - {self.text}"
class Answer(models.Model):
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name='answers',
        verbose_name='Question'
    )
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='answers')
    text = models.TextField(verbose_name='Answer Text')
    upvotes = models.PositiveIntegerField(default=0, verbose_name='Upvotes')
    downvotes = models.PositiveIntegerField(default=0, verbose_name='Downvotes')
    votes = models.IntegerField(default=0, verbose_name='Net Votes')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-votes', '-created_at']
        verbose_name = 'Answer'
        verbose_name_plural = 'Answers'

    def __str__(self):
        return f"Answer to: {self.question.text[:40]}..."


class Comment(models.Model):
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Question'
    )
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='comments')
    text = models.TextField(verbose_name='Comment Text')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'

    def __str__(self):
        return f"Comment on: {self.question.text[:40]}..."
