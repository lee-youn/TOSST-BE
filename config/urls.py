"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static

from django.urls import path, include
from user.views import register, login, user, user_wake, wake_status_monthly
from group.views import group, user_group, group_data, group_user_list, group_list, group_user_status
from todo.views import todo_create, todo_updateDelete
from news.views import news, news_quiz, quiz_status

urlpatterns = [
    path("admin/", admin.site.urls),
    path("register/", register),
    path("login/", login),
    path("user/", user),
    path("group/", group),
    path("user/group/", user_group),
    path('group/<int:id>/', group_data),
    path('group/user_list/', group_user_list),
    path('group/list/', group_list),
    path('group/user_status/', group_user_status),
    path("todos/", todo_create),
    path('todos/<int:id>/', todo_updateDelete),
    path('user/wake/', user_wake),
    path('news/', news),
    path('news/quizzes/', news_quiz),
    path('news/quiz/', quiz_status),
    path('user/month/', wake_status_monthly)
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)