from datetime import date, timedelta

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.core.cache import cache
from django.core.serializers.json import DjangoJSONEncoder
import json


from django.http import JsonResponse
from django.urls import reverse

from .models import ChatboxMessage

import LogMyFit.forms as forms
from capstoneproject.utils.create_leaderboard_metrics import create_leaderboard_metrics
from .models import Activity, Goal, UserProfile
from capstoneproject.utils import get_activities_for_user, get_goals_for_user


def home(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    else:
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
    boards = cache.get('leaderboard_metrics')
    if boards is None:
        boards = create_leaderboard_metrics()

    # Format metric names for better display in UI
    formatted_leaderboards = {
        metric.replace("_", " ").title(): ranking_list
        for metric, ranking_list in boards.items()
    }

    return render(request, 'leaderboards.html', {'leaderboards': formatted_leaderboards})

@login_required
def clear_leaderboard_cache(request):
    cache.delete('leaderboard_metrics')
    return redirect('leaderboards')

def login(request):
    return render(request, 'login.html')


@login_required
def profile_view(request, username):
    cache_key = f"profile_{username}"
    context = cache.get(cache_key)
    if context is None:
        profile_user = get_object_or_404(User, username=username)
        profile, created = UserProfile.objects.get_or_create(user=profile_user)
        is_owner = (profile_user == request.user)

        context = {'profile_user': profile_user,
               'is_owner': is_owner,
               'js_get_chats_url': request.build_absolute_uri(reverse('get_chats')),
                'js_post_chat_url': request.build_absolute_uri(reverse('post_chat')),
                'recipient_id': profile_user.id,
                'profile': profile,
        }
        cache.set(cache_key, context, 300) #300 seconds
        #Updating the profile requires invalidating this cached object
    return render(request, 'profile.html', context)


def update_theme(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = forms.ThemeForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile', username=request.user.username)
    else:
        form = forms.ThemeForm(instance=profile)

    return render(request, 'profile.html', {
        'profile_user': request.user,
        'is_owner': True,
        'form': form
    })
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

    # This is just an example, expand relevant data structures and visualization_data for send to dashboard.html
    # intermediate data structures are not sent
    workout_activities = [activity for activity in monthly_activities if activity.activityType == 'Workout']
    # a more complicated example
    """total_miles_cycled = sum(
    (activity.workout_activity.distance or 0)
    for activity in monthly_activities
    if activity.activityType == 'Workout'
       and hasattr(activity, 'workout_activity')
       and activity.workout_activity.exerciseType == 'Cycling'
    )"""

    # visualizations data is sent as context to template
    visualization_data = {
        'total_activities': len(monthly_activities),
        'total_workout_activities': len(workout_activities),
        #total_miles_cycled: total_miles_cycled
    }

    # For Visualization
    chart_data = {
        'calories': [],
        'dates': [],
        'water': [],
        'sleep': [],
        'workout_duration': []
    }

    # For Visualization
    for act in monthly_activities:
        date_label = act.activity_date.strftime('%Y %m, %d')
        chart_data['dates'].append(date_label)

        if act.activityType == 'Meal' and hasattr(act, 'meal_activity'):
            chart_data['calories'].append(act.meal_activity.calories)
        else:
            chart_data['calories'].append(0)

        if act.activityType == 'Water' and hasattr(act, 'water_activity'):
            chart_data['water'].append(act.water_activity.amount)
        else:
            chart_data['water'].append(0)

        if act.activityType == 'Sleep' and hasattr(act, 'sleep_activity'):
            sleep_duration = act.sleep_activity.duration.total_seconds() / 3600
            chart_data['sleep'].append(round(sleep_duration, 2))
        else:
            chart_data['sleep'].append(0)

        if act.activityType == 'Workout' and hasattr(act, 'workout_activity'):
            chart_data['workout_duration'].append(act.workout_activity.duration or 0)
        else:
            chart_data['workout_duration'].append(0)

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
        'visualization_data': visualization_data,
        'chart_data_json': json.dumps(chart_data, cls=DjangoJSONEncoder)
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

@login_required
def post_chat(request):  #Receives POST via AJAX with a new message.
    if request.method == 'POST':
        message_text = request.POST.get('message', '').strip()
        recipient_id = request.POST.get('recipient')
        if message_text and recipient_id:
            recipient = get_object_or_404(User, pk=recipient_id)
            ChatboxMessage.objects.create(
                recipient=recipient,
                sender=request.user,
                message=message_text
            )
            cache_key = f"chat_messages_{recipient_id}"
            cache.delete(cache_key)
            return JsonResponse({'status': 'ok'})
        return JsonResponse({'status': 'error', 'message': 'Missing message or recipient'}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=405)

def get_chats(request): #Returns the latest chatbox messages as JSON.
    recipient_id = request.GET.get("recipient")
    if recipient_id:
        try:
            recipient = User.objects.get(pk=recipient_id)
        except User.DoesNotExist:
            recipient = request.user
    else:
        recipient = request.user
    cache_key = f"chat_messages_{recipient.id}"
    messages = cache.get(cache_key)

    if messages is None:
        messages_query = ChatboxMessage.objects.filter(recipient_id=recipient_id).order_by('-timestamp')[:20]
        messages = []
        for m in messages_query:
            messages.append({
                'sender': m.sender.username if m.sender else 'Anonymous',
                'message': m.message,
                'timestamp': m.timestamp.strftime("%Y-%m-%d %H:%M:%S")
            })
        cache.set(cache_key, messages, 300)

    return JsonResponse({'messages': messages})