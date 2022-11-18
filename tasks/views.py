from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from tasks.models import Task
from .form import TaskCreate
from django.utils import timezone
from django.contrib.auth.decorators import login_required


def home_page(request):
    return render(request, 'home.html')


def signup(request):
    if request.method == "GET":
        return render(request, 'signup.html', {"form": UserCreationForm})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(username=request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('tasks')
            except IntegrityError:
                return render(request, 'signup.html', {"form": UserCreationForm,
                                                       "error": "User already exists"})
        else:
            return render(request, 'signup.html', {"form": UserCreationForm,
                                                   "error": "Password do not match"})


@login_required()
def tasks(request):
    task = Task.objects.filter(user=request.user)
    return render(request, 'tasks.html', {'task': task})


@login_required()
def signout(request):
    logout(request)
    return redirect('home')


@login_required()
def create_task(request):
    if request.method == "GET":
        return render(request, 'create_task.html', {'form': TaskCreate})
    else:
        try:
            form = TaskCreate(request.POST)
            new_task = form.save(commit=False)
            new_task.user = request.user
            new_task.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'create_task.html', {'form': TaskCreate,
                                                        'error': 'Try again'})


@login_required()
def task_detail(request, task_id):
    if request.method == "GET":
        task = get_object_or_404(Task, id=task_id, user=request.user)
        form = TaskCreate(instance=task)
        return render(request, 'task_detail.html', {'task': task,
                                                    'form': form})
    else:
        try:
            update_task = get_object_or_404(Task, id=task_id, user=request.user)
            form = TaskCreate(request.POST, instance=update_task)
            form.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'task_detail.html', {'error': 'Update invalid'})


@login_required()
def task_complete(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    if request.method == "POST":
        task.date_completed = timezone.now()
        task.save()
        return redirect('tasks')


@login_required()
def get_comp_tasks(request):
    tasks = Task.objects.filter(user=request.user)
    return render(request, 'complete_tasks.html', {'tasks': tasks})


@login_required()
def task_delete(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    if request.method == "POST":
        task.delete()
        return redirect('tasks')


def signin(request):
    if request.method == "GET":
        return render(request, 'signin.html', {'form': AuthenticationForm})
    else:
        user = authenticate(request, username=request.POST["username"], password=request.POST['password'])
        if user is None:
            return render(request, 'signin.html', {'form': AuthenticationForm,
                                                   'error': "User or password is wrong"})
        else:
            login(request, user)
            return redirect('tasks')
