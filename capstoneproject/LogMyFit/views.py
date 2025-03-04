from datetime import date

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import RegistrationForm, ActivityForm, WorkoutActivityForm, MealActivityForm, WaterActivityForm, SleepActivityForm
from .models import Activity, WorkoutActivity, MealActivity, WaterActivity, SleepActivity


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
        # Get the activity type from the hidden input field
        activity_type = request.POST.get('activityType')

        # Initialize the form based on the activity type
        if activity_type == 'Workout':
            form = WorkoutActivityForm(request.POST)
        elif activity_type == 'Meal':
            form = MealActivityForm(request.POST)
        elif activity_type == 'Water':
            form = WaterActivityForm(request.POST)
        elif activity_type == 'Sleep':
            form = SleepActivityForm(request.POST)
        else:
            form = None

        # Get the activity_date from the form or default to the current date
        activity_date = request.POST.get('activity_date') or date.today()

        # Save the form if it's valid
        if form and form.is_valid():
            # Create the Activity object first
            activity = Activity.objects.create(
                user=request.user,
                activityType=activity_type,
                activity_date=activity_date  # Assign the activity date
            )

            # Now set the activity foreign key for the form (i.e., link the Activity)
            activity_instance = form.save(commit=False)
            activity_instance.activity = activity  # Link the specific activity to the Activity object
            activity_instance.save()  # Save the specific activity (e.g., WorkoutActivity, MealActivity, etc.)

            # Redirect to the dashboard after successful submission
            return redirect('dashboard')

    else:
        # Initialize forms for each activity
        workout_form = WorkoutActivityForm()
        meal_form = MealActivityForm()
        water_form = WaterActivityForm()
        sleep_form = SleepActivityForm()

    # Get all activities for the current user
    activities = Activity.objects.filter(user=request.user).select_related(
        'workout_activity', 'meal_activity', 'water_activity', 'sleep_activity'
    )

    return render(request, 'dashboard.html', {
        'workout_form': workout_form,
        'meal_form': meal_form,
        'water_form': water_form,
        'sleep_form': sleep_form,
        'activities': activities
    })
