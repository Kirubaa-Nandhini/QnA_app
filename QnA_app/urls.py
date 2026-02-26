"""
URL configuration for QnA_app project.
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('questions/', include('questions.urls', namespace='questions')),
    path('', RedirectView.as_view(url='/questions/', permanent=False)),
]
