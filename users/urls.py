from django.urls import path, include
from . import views

urlpatterns = [
	path("", views.profile, name='profile'),
	path("edit/<int:pk>", views.edit, name='edit-post'),
]