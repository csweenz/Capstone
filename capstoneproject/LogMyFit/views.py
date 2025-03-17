from datetime import date, timedelta
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
        activity_type = request.POST.get('activityType')
        activity_date = request.POST.get('activity_date') or date.today()

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

        if form and form.is_valid():
            activity = Activity.objects.create(
                user=request.user,
                activityType=activity_type,
                activity_date=activity_date
            )
            activity_instance = form.save(commit=False)
            activity_instance.activity = activity
            activity_instance.save()
            return redirect('dashboard')

    else:
        workout_form = WorkoutActivityForm()
        meal_form = MealActivityForm()
        water_form = WaterActivityForm()
        sleep_form = SleepActivityForm()

    activities = Activity.objects.filter(user=request.user).select_related(
        'workout_activity', 'meal_activity', 'water_activity', 'sleep_activity'
    )

    # 30 days of data for visualization
    series_30_date = date.today() - timedelta(days=30)
    monthly_activities = Activity.objects.filter(user=request.user, activity_date__gte=series_30_date)

    # This is just an example, expand visualization_data for send to dashboard.html
    visualization_data = {
        'total_activities': monthly_activities.count(),
        'total_workout_activities': monthly_activities.filter(activityType='Workout').count(),
    }

    return render(request, 'dashboard.html', {
        'workout_form': workout_form,
        'meal_form': meal_form,
        'water_form': water_form,
        'sleep_form': sleep_form,
        'activities': activities,
        'visualization_data': visualization_data
    })

@login_required
def delete_activity(request, activity_id):
    activity = get_object_or_404(Activity, activityID=activity_id, user=request.user)

    # checking if related activity exists before deleting
    if activity.activityType == 'Workout' and hasattr(activity, 'workout_activity'):
        activity.workout_activity.delete()
    elif activity.activityType == 'Meal' and hasattr(activity, 'meal_activity'):
        activity.meal_activity.delete()
    elif activity.activityType == 'Water' and hasattr(activity, 'water_activity'):
        activity.water_activity.delete()
    elif activity.activityType == 'Sleep' and hasattr(activity, 'sleep_activity'):
        activity.sleep_activity.delete()

    # deletes the main Activity entry
    activity.delete()

    return redirect('dashboard')


@login_required
def edit_activity(request, activity_id):
    activity = get_object_or_404(Activity, activityID=activity_id, user=request.user)

    # initialize the form for editing based on the activity type
    if activity.activityType == 'Workout' and hasattr(activity, 'workout_activity'):
        form = WorkoutActivityForm(instance=activity.workout_activity)
    elif activity.activityType == 'Meal' and hasattr(activity, 'meal_activity'):
        form = MealActivityForm(instance=activity.meal_activity)
    elif activity.activityType == 'Water' and hasattr(activity, 'water_activity'):
        form = WaterActivityForm(instance=activity.water_activity)
    elif activity.activityType == 'Sleep' and hasattr(activity, 'sleep_activity'):
        form = SleepActivityForm(instance=activity.sleep_activity)
    else:
        form = None

    if request.method == 'POST' and form:
        # making sure that the form is initialized with the POST data and the correct instance
        form = form.__class__(request.POST,
                              instance=activity.workout_activity if activity.activityType == 'Workout' else
                              activity.meal_activity if activity.activityType == 'Meal' else
                              activity.water_activity if activity.activityType == 'Water' else
                              activity.sleep_activity)
        if form.is_valid():
            form.save()
            return redirect('dashboard')  # after saving it will redirect the user back to the dashboard

    return render(request, 'edit_activity.html', {'form': form, 'activity': activity})