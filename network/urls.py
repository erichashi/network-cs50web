
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),

    #for the page
    path("following", views.following, name="following"),
    #for adding or removing
    path("follow/<int:user_id>", views.follow, name="follow"),

    path("compose", views.new, name="new"),

    #API routes
    path("api/posts/new", views.compose, name="compose"),
    path("api/posts/<int:post_id>", views.post, name="post"),

    path("<str:username>", views.profile, name="profile"),

]
