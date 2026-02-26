from django.db import models


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
    choice1 = models.CharField(max_length=255, blank=True, default='', verbose_name='Choice 1')
    choice2 = models.CharField(max_length=255, blank=True, default='', verbose_name='Choice 2')
    choice3 = models.CharField(max_length=255, blank=True, default='', verbose_name='Choice 3')
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
