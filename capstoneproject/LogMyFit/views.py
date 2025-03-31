from datetime import date, timedelta

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.core.cache import cache

import LogMyFit.forms as forms
from capstoneproject.utils.create_leaderboard_metrics import create_leaderboard_metrics
from .models import Activity, Goal
from capstoneproject.utils import get_activities_for_user, get_goals_for_user


def home(request):
    return render(request, 'home.html')


def success(request):
    return render(request, 'success.html')


def add_user(request):
    if request.method == 'POST':
        form = forms.RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('success')
    else:
        form = forms.RegistrationForm()

    return render(request, 'add_user.html', {'form': form})


def user_list(request):
    users = cache.get('all_users')
    if users is None:
        users = list(User.objects.all().values('username', 'email')) # list instead of queryset to prevent iterating over queryset
        cache.set('all_users', users, 900) # 15 minutes (900 seconds)
    return render(request, 'user_list.html', {'users': users})

def leaderboards(request):
    boards = cache.get('leaderboard')
    if boards is None:
        boards = create_leaderboard_metrics()
    return render(request, 'leaderboards.html', {'leaderboards': boards})

def login(request):
    return render(request, 'login.html')


@login_required
def dashboard(request):
    if request.method == 'POST':
        form_type = request.POST.get('form_type')

        if form_type == 'activity':
            activity_type = request.POST.get('activityType')
            activity_date = request.POST.get('activity_date') or date.today()

            if activity_type == 'Workout':
                form = forms.WorkoutActivityForm(request.POST)
            elif activity_type == 'Meal':
                form = forms.MealActivityForm(request.POST)
            elif activity_type == 'Water':
                form = forms.WaterActivityForm(request.POST)
            elif activity_type == 'Sleep':
                form = forms.SleepActivityForm(request.POST)
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
                cache.delete(f'activities_{request.user}')
                cache.delete(f'activities_{request.user}_30_days')
                return redirect('dashboard')

        if form_type == 'goal':
            goal_type = request.POST.get('goal_type')

            if goal_type == 'Fitness':
                form = forms.FitnessGoalForm(request.POST)
            elif goal_type == 'Nutrition':
                form = forms.NutritionGoalForm(request.POST)
            elif goal_type == 'Water':
                form = forms.WaterGoalForm(request.POST)
            elif goal_type == 'Sleep':
                form = forms.SleepGoalForm(request.POST)
            else:
                form = None

            if form and form.is_valid():
                days_until_deadline = form.cleaned_data.get('targetDate')
                deadline = date.today() + timedelta(days=days_until_deadline)
                goal = Goal.objects.create(
                    user=request.user,
                    goalType=goal_type,
                    targetDate=deadline)
                goal_instance = form.save(commit=False)
                goal_instance.goal = goal
                goal_instance.save()
                cache.delete(f'goals_{request.user}')
                return redirect('dashboard')
    else:
        workout_form = forms.WorkoutActivityForm()
        meal_form = forms.MealActivityForm()
        water_form = forms.WaterActivityForm()
        sleep_form = forms.SleepActivityForm()
        fitness_goal_form = forms.FitnessGoalForm()
        nutrition_goal_form = forms.NutritionGoalForm()
        water_goal_form = forms.WaterGoalForm()
        sleep_goal_form = forms.SleepGoalForm()


    activities = get_activities_for_user.get_all(request)
    monthly_activities = get_activities_for_user.get_monthly(request)
    goals = get_goals_for_user.get_goals(request)

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
        'fitness_goal_form': fitness_goal_form,
        'nutrition_goal_form': nutrition_goal_form,
        'water_goal_form': water_goal_form,
        'sleep_goal_form': sleep_goal_form,
        'activities': activities,
        'monthly_activities': monthly_activities,
        'goals' : goals,
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
    cache.delete(f'activities_{request.user}')
    cache.delete(f'activities_{request.user}_30_days')

    return redirect('dashboard')


@login_required
def edit_activity(request, activity_id):
    activity = get_object_or_404(Activity, activityID=activity_id, user=request.user)

    # initialize the form for editing based on the activity type
    if activity.activityType == 'Workout' and hasattr(activity, 'workout_activity'):
        form = forms.WorkoutActivityForm(instance=activity.workout_activity)
    elif activity.activityType == 'Meal' and hasattr(activity, 'meal_activity'):
        form = forms.MealActivityForm(instance=activity.meal_activity)
    elif activity.activityType == 'Water' and hasattr(activity, 'water_activity'):
        form = forms.WaterActivityForm(instance=activity.water_activity)
    elif activity.activityType == 'Sleep' and hasattr(activity, 'sleep_activity'):
        form = forms.SleepActivityForm(instance=activity.sleep_activity)
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
            cache.delete(f'activities_{request.user}')
            cache.delete(f'activities_{request.user}_30_days')
            return redirect('dashboard')  # after saving it will redirect the user back to the dashboard

    return render(request, 'edit_activity.html', {'form': form, 'activity': activity})

@login_required
def delete_goal(request, goal_id):
    goal = get_object_or_404(Goal, goalID=goal_id, user=request.user)

    # checking if related goal exists before deleting
    if goal.goalType == 'Fitness' and hasattr(goal, 'fitness_goal'):
        goal.fitness_goal.delete()
    elif goal.goalType == 'Nutrition' and hasattr(goal, 'nutrition_goal'):
        goal.nutrition_goal.delete()
    elif goal.goalType == 'Water' and hasattr(goal, 'water_goal'):
        goal.water_goal.delete()
    elif goal.goalType == 'Sleep' and hasattr(goal, 'sleep_goal'):
        goal.sleep_goal.delete()

    goal.delete()
    cache.delete(f'goals_{request.user}')
    return redirect('dashboard')

@login_required
def edit_goal(request, goal_id):
    goal = get_object_or_404(Goal, goalID=goal_id, user=request.user)

    # Determine the appropriate form class and instance based on the goal type.
    if goal.goalType == 'Fitness' and hasattr(goal, 'fitness_goal'):
        form_class = forms.FitnessGoalForm
        instance = goal.fitness_goal
    elif goal.goalType == 'Nutrition' and hasattr(goal, 'nutrition_goal'):
        form_class = forms.NutritionGoalForm
        instance = goal.nutrition_goal
    elif goal.goalType == 'Water' and hasattr(goal, 'water_goal'):
        form_class = forms.WaterGoalForm
        instance = goal.water_goal
    elif goal.goalType == 'Sleep' and hasattr(goal, 'sleep_goal'):
        form_class = forms.SleepGoalForm
        instance = goal.sleep_goal
    else:
        form_class = None
        instance = None

    if form_class is None:
        return redirect('dashboard')

    if request.method == 'POST':
        form = form_class(request.POST, instance=instance)
        if form.is_valid():
            target_value = form.cleaned_data.get('targetDate')
            new_deadline = date.today() + timedelta(days=target_value)
            goal.targetDate = new_deadline
            goal.save()
            form.save()
            cache.delete(f'goals_{request.user}')
            return redirect('dashboard')
    else:
        form = form_class(instance=instance)

    return render(request, 'edit_goal.html', {'form': form, 'goal': goal})

@login_required
def toggle_goal_status(request, goal_id):
    goal = get_object_or_404(Goal, goalID=goal_id, user=request.user)
    if goal.status == 'Active':
        goal.status = 'Completed'
    else:
        goal.status = 'Active'
    goal.save()
    cache.delete(f'goals_{request.user}')
    return redirect('dashboard')