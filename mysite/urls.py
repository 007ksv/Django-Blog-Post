"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include		#include() used for including the views
from users import views as users_view
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('polls.urls')),
    path("register/", users_view.register, name='register'),
    path("logout/", users_view.logout, name='logout'),
    path("new-post/", users_view.newPost, name='new-post'),
    path("profile/", include('users.urls')),
    path('user-profile/<str:username>/', users_view.fetchProfile, name='user-profile'),
    path('change-password/', users_view.changePassword, name='change-password'),
    path('update-profile/', users_view.editProfile, name='edit-profile'),
    path('remove-post/<int:pid>', users_view.removePost, name='remove-post'),
    path('post-detail/<int:pid>', users_view.post_detail, name='post-detail'),
    path('like_post/', users_view.like, name='like_post'),
    path('favourite-post', users_view.favourite, name='favourite-post'),
    path('list-favourites', users_view.list_favourites, name='list-favourites'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)