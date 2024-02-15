from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.db import IntegrityError
from .forms import CreateTask
from .models import Task

# Create your views here.
# Home view
def home(request):
    return render(request, 'home.html')

# Signup view
def signup(request):
    if request.method == 'GET':
        return render(request, 'logins/signup.html', {
        'form': UserCreationForm 
        })
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(username=request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('task')
            except IntegrityError:
                return render(request, 'logins/signup.html', {
                    'form': UserCreationForm,
                    'error': 'Username already exists'
                })
        else:
            return render(request, 'logins/signup.html', {
                'form': UserCreationForm,
                'error': 'Password do not match'
            })

def signout(request):
    logout(request)
    return redirect('home')

def signin(request):
    if request.method == 'GET':
        return render(request, 'logins/signin.html', {
            'form': AuthenticationForm
        })
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'logins/signin.html', {
                'error': 'Username and password do not match',
                'form': AuthenticationForm
            })
        else:
            login(request, user)
            return redirect('task')
        

def task(request):
    tasks = Task.objects.filter(user=request.user).order_by('-created')
    return render(request, 'task/task.html', {'tasks': tasks})

def taskDetail(request, id):
    task = get_object_or_404(Task, id=id)
    return render(request, 'task/task_detail.html', {'task': task})

def createTask(request):
    if request.method == 'GET':
        return render(request, 'task/create_task.html', {
            'form': CreateTask
        })
    else:
        try:
            form = CreateTask(request.POST)
            newtask = form.save(commit=False)
            newtask.user = request.user
            newtask.save()
            return redirect('task')
        except ValueError:
            return render(request, 'task/create_task.html', {
                'error': 'Bad data passed in. Try again.',
                'form': CreateTask
            })