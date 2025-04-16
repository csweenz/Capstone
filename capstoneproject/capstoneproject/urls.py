"""
URL configuration for capstoneproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from django.views.generic import RedirectView

from LogMyFit import views
from LogMyFit.views import home, success, add_user, user_list, dashboard
from LogMyFit.views import edit_activity

urlpatterns = [
    path('', home, name='home'),
    path('admin/', admin.site.urls),
    path('add-user/', add_user, name='add_user'),
    path('user-list/', user_list, name='user_list'),
    path('leaderboards/', views.leaderboards, name='leaderboards'),
    path('clear-leaderboard/', views.clear_leaderboard_cache, name='clear_leaderboard_cache'),
    path('success/', success, name='success'),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('accounts/login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('dashboard/', dashboard, name='dashboard'),
    path('edit_activity/<int:activity_id>/', views.edit_activity, name='edit_activity'),
    path('delete_activity/<int:activity_id>/', views.delete_activity, name='delete_activity'),
    path('edit_goal/<int:goal_id>/', views.edit_goal, name='edit_goal'),
    path('delete_goal/<int:goal_id>/', views.delete_goal, name='delete_goal'),
    path('goal/toggle/<int:goal_id>/', views.toggle_goal_status, name='toggle_goal_status'),
    path('profile/<str:username>/', views.profile_view, name='profile'),
    path('update-theme/', views.update_theme, name='update_theme'),
    path('chatbox/post/', views.post_chat, name='post_chat'),
    path('chatbox/messages', views.get_chats, name='get_chats'),

]