from datetime import date
from gc import get_objects

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import RegistrationForm, ActivityForm, WorkoutActivityForm, MealActivityForm, WaterActivityForm, SleepActivityForm
from .models import Activity, WorkoutActivity, MealActivity, WaterActivity, SleepActivity
from django.shortcuts import get_object_or_404


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

@login_required
def delete_activity(request, activity_id):
    activity = get_object_or_404(Activity, id=activity_id, user=request.user)

    # Check if related activity exists before deleting
    if activity.activityType == 'Workout' and hasattr(activity, 'workout_activity'):
        activity.workout_activity.delete()
    elif activity.activityType == 'Meal' and hasattr(activity, 'meal_activity'):
        activity.meal_activity.delete()
    elif activity.activityType == 'Water' and hasattr(activity, 'water_activity'):
        activity.water_activity.delete()
    elif activity.activityType == 'Sleep' and hasattr(activity, 'sleep_activity'):
        activity.sleep_activity.delete()

    # Delete the main Activity entry
    activity.delete()

    return redirect('dashboard')


@login_required
def edit_activity(request, activity_id):
    activity = get_object_or_404(Activity, id=activity_id, user=request.user)

    # Determine the correct form to use based on activity type
    form = None
    if activity.activityType == 'Workout' and hasattr(activity, 'workout_activity'):
        form = WorkoutActivityForm(instance=activity.workout_activity)
    elif activity.activityType == 'Meal' and hasattr(activity, 'meal_activity'):
        form = MealActivityForm(instance=activity.meal_activity)
    elif activity.activityType == 'Water' and hasattr(activity, 'water_activity'):
        form = WaterActivityForm(instance=activity.water_activity)
    elif activity.activityType == 'Sleep' and hasattr(activity, 'sleep_activity'):
        form = SleepActivityForm(instance=activity.sleep_activity)

    if request.method == 'POST' and form:
        form = form.__class__(request.POST, instance=form.instance)  # Corrected instance access
        if form.is_valid():
            form.save()
            return redirect('dashboard')

    return render(request, 'edit_activity.html', {'form': form, 'activity': activity})