from django.db import IntegrityError
from django.http import Http404
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .forms import TodoForm, ModifyUserCreationForm
from .models import Todo


def home(request):
    return render(request, 'todo/home.html')


def signupuser(request):
    if request.method == "GET":
        return render(request, 'todo/signupuser.html', {'form': ModifyUserCreationForm(auto_id='id_for_%s')})
    else:
        form = ModifyUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            user = User.objects.get(username=request.POST['username'])
            login(request, user)
            return redirect('currenttodos')
        else:
            return render(request, 'todo/signupuser.html',
                          {'form': ModifyUserCreationForm(request.POST, auto_id='id_for_%s')})


def current_todos(request):
    todos = Todo.objects.filter(user=request.user, datecomplited__isnull=True)
    return render(request, 'todo/currenttodos.html', {'todos': todos})


@login_required
def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')


def loginuser(request):
    if request.method == "GET":
        return render(request, 'todo/loginuser.html', {'form': AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'todo/loginuser.html',
                          {'form': AuthenticationForm(), 'error': '''username and passwords didn't match'''})
        else:
            login(request, user)
            return redirect('currenttodos')


@login_required
def create_todos(request):
    if request.method == 'GET':
        return render(request, 'todo/createtodos.html', {'form': TodoForm})
    else:
        form = TodoForm(request.POST)
        newtodo = form.save(commit=False)
        newtodo.user = request.user
        try:
            newtodo.save()
        except ValueError:
            return render(request, 'todo/createtodos.html', {'form': TodoForm, 'errors': 'bad data passed in'})
    return redirect('currenttodos')


@login_required
def detail_todo(request, todonumber):
    if request.method == 'GET':
        try:
            todo = Todo.objects.filter(user=request.user)
            todo = todo[todonumber - 1]
        except BaseException:
            raise Http404
        else:
            form = TodoForm(instance=todo)
            return render(request, 'todo/tododetail.html', {'todo': todo, 'form': form, 'idx': todonumber})
    else:
        todo = Todo.objects.filter(user=request.user)
        todo = todo[todonumber - 1]
        form = TodoForm(request.POST, instance=todo)
        form.save()
        return redirect('detailtodo', todonumber=todonumber)


@login_required
def complete_todo(request, todonumber):
    if request.method == 'GET':
        raise Http404
    todo = Todo.objects.filter(user=request.user)
    todo = todo[todonumber - 1]
    todo.datecomplited = timezone.now()
    todo.save()
    return redirect('currenttodos')


@login_required
def delete_todo(request, todonumber):
    if request.method == 'GET':
        raise Http404
    todo = Todo.objects.filter(user=request.user)
    todo = todo[todonumber - 1]
    todo.delete()
    return redirect('currenttodos')


@login_required
def complited(request):
    try:
        todos = Todo.objects.filter(user=request.user, datecomplited__isnull=False).order_by('-datecomplited')
    except BaseException:
        return render(request, 'todo/comlited.html', {'massege': 'You have no complited Tasks'})
    return render(request, 'todo/comlited.html', {'todos': todos})
