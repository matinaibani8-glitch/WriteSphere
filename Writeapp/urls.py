from django.contrib import admin
from django.urls import path
from Writeapp import views

urlpatterns = [
    path("",views.index,name="home"),
    path("signup/",views.signup,name="signup"),
    path("login/",views.login,name="login"),
    path("create/",views.create,name="create"),
    path("profile/",views.profile,name="profile"),
    path("blog/",views.blog,name="blog"),
    path("userlogout/",views.userlogout,name="logout"),
    path('post/<int:post_id>/like/',views.like_post,name='like_post'),
    path('post/<int:post_id>/comment/',views.add_comment,name='add_comment'),
    path("Edit/<int:id>/",views.Edit,name="edit"),
    path("delete/<int:id>/",views.delete,name="Delete"),
    path("EditP/<int:id>/",views.ed_profile,name="Profile_Edit"),
    path("search/",views.search,name="search"),
    path("follow/<int:id>/",views.follow_user,name="follow_user"),
    path("category/",views.category,name="category"),
    path("author_search/",views.author_search,name="author_search"),
]
