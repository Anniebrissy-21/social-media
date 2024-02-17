"""
URL configuration for socialmedia project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path

from django.conf import settings
from django.conf.urls.static import static

from myapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("",views.SignInView.as_view(),name="login"),
    path("register",views.SignUpView.as_view(),name="signup"),
    path("signout",views.SignOutView.as_view(),name="logout"),
    path("index",views.IndexView.as_view(),name="index"),
    path("profiles",views.ProfileCreateView.as_view(),name="profile"),
    path("profiles/<int:pk>",views.ProfileDetailView.as_view(),name="profile-detail"),
    path("profile/<int:pk>/change",views.ProfileEditView.as_view(),name="profile-edit"),
    path("posts",views.PostCreateView.as_view(),name="post-add"),
    path("posts/<int:pk>/change",views.PostEditView.as_view(),name="post-edit"),
    path("posts/<int:pk>/delete",views.PostDeleteView.as_view(),name="post-delete"),
    path("posts/<int:pk>/liked",views.PostLikeView.as_view(),name="post-like"),
    path("posts/<int:pk>/saved",views.PostSaveView.as_view(),name="post-save"),
    path("posts/<int:pk>/liked/all",views.LikedPostListView.as_view(),name="liked-post"),
    path("stories",views.StoryCreateView.as_view(),name="story-add"),
    path("stories/<int:pk>/delete",views.StoryDeleteView.as_view(),name="story-delete"),
    path("posts/<int:pk>/comments",views.CommentCreateView.as_view(),name="comment"),
    path("comments/<int:pk>/delete",views.CommentDeleteView.as_view(),name="comment-delete")
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
