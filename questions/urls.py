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
]
