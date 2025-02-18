from django.shortcuts import render, redirect
from .forms import  RegistrationForm
from django.contrib.auth.models import User

def home(request):
    return render(request, 'home.html')

def success(request):
    return render(request, 'success.html')


def add_user(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()  # This saves the user to the database
            return redirect('success')  # Redirect to a success page or somewhere else
    else:
        form = RegistrationForm()

    return render(request, 'add_user.html', {'form': form})

def user_list(request):
    users = User.objects.all()  # Retrieve all users from the database
    return render(request, 'user_list.html', {'users': users})


