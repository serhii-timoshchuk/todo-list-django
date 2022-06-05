"""djangoTodo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from todo import views

urlpatterns = [
    path('admin/', admin.site.urls),

    #Auth
    path('signup/', views.signupuser, name='signupuser'),
    path('login/', views.loginuser, name='loginuser'),
    path('logout/', views.logoutuser, name='logoutuser'),

    #Todos
    path('', views.home, name='home'),
    path('current/', views.current_todos, name='currenttodos'),
    path('complited/', views.complited, name='complited'),
    path('create-todos/', views.create_todos, name='createtodos'),
    path('todo-<int:idx>', views.detail_todo, name='detailtodo'),
    path('todo-<int:idx>/complete', views.complete_todo, name='completetodo'),
    path('todo-<int:idx>/deletet', views.delete_todo, name='deletetodo'),
]
