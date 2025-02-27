from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import RegistrationForm, ActivityForm
from .models import Activity
from django.utils import timezone


def home(request):
    return render(request, 'home.html')


def success(request):
    return render(request, 'success.html')


def add_user(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('success')
    else:
        form = RegistrationForm()

    return render(request, 'add_user.html', {'form': form})


def user_list(request):
    users = User.objects.all()
    return render(request, 'user_list.html', {'users': users})


def login(request):
    return render(request, 'login.html')


@login_required
def dashboard(request):
    if request.method == 'POST':
        form = ActivityForm(request.POST)
        if form.is_valid():
            activity = form.save(commit=False)
            activity.user = request.user

            activity.save()
            return redirect('dashboard')
    else:
        form = ActivityForm()

    activities = Activity.objects.filter(user=request.user)

    return render(request, 'dashboard.html', {'activities': activities, 'form': form})