from django.urls import path
from . import views

app_name = 'questions'

urlpatterns = [
    path('', views.QuestionListView.as_view(), name='list'),
    path('create/', views.QuestionCreateView.as_view(), name='create'),
    path('<int:pk>/edit/', views.QuestionUpdateView.as_view(), name='edit'),
    path('<int:pk>/delete/', views.QuestionDeleteView.as_view(), name='delete'),
    path('<int:pk>/', views.QuestionDetailView.as_view(), name='detail'),
    path('<int:pk>/like/', views.like_question, name='like'),
    path('<int:pk>/answer/', views.create_answer, name='create_answer'),
    path('<int:pk>/comment/', views.create_comment, name='create_comment'),
    path('answer/<int:pk>/upvote/', views.upvote_answer, name='upvote_answer'),
    path('answer/<int:pk>/downvote/', views.downvote_answer, name='downvote_answer'),
    path('answer/<int:pk>/edit/', views.AnswerUpdateView.as_view(), name='answer_edit'),
    path('answer/<int:pk>/delete/', views.AnswerDeleteView.as_view(), name='answer_delete'),
]
