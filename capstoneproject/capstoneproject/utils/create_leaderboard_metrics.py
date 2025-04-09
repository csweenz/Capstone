from datetime import date, timedelta
from django.core.cache import cache
from django.db.models import Sum, Min, F, ExpressionWrapper, FloatField
from django.contrib.auth.models import User
from LogMyFit.models import Activity, WorkoutActivity, MealActivity, WaterActivity, SleepActivity, Goal

def create_leaderboard_metrics():
    user_metrics = []
    users = User.objects.all()

    for user in users:
        # Fitness metrics
        total_workouts = Activity.objects.filter(user=user, activityType='Workout').count()
        distance_ran = (
            WorkoutActivity.objects.filter(activity__user=user, exerciseType='Running')
            .aggregate(total=Sum('distance'))['total'] or 0
        )
        distance_swam = (
            WorkoutActivity.objects.filter(activity__user=user, exerciseType='Swimming')
            .aggregate(total=Sum('distance'))['total'] or 0
        )
        distance_cycled = (
            WorkoutActivity.objects.filter(activity__user=user, exerciseType='Cycling')
            .aggregate(total=Sum('distance'))['total'] or 0
        )

        # Meals
        meals_tracked = MealActivity.objects.filter(activity__user=user).count()
        carb_expr = ExpressionWrapper(
            F('carbs') / (F('carbs') + F('fat') + F('protein')) * 100,
            output_field=FloatField()
        )
        lowest_carb_percentage = (
            MealActivity.objects.filter(activity__user=user)
            .aggregate(lowest=Min(carb_expr))['lowest'] or 100
        )

        # Water
        water_logs = WaterActivity.objects.filter(activity__user=user).count()
        amount_drank = (
            WaterActivity.objects.filter(activity__user=user)
            .aggregate(total=Sum('amount'))['total'] or 0
        )

        # Sleep
        sleep_activities = list(SleepActivity.objects.filter(activity__user=user).select_related('activity'))
        total_sleep_seconds = sum(s.duration.total_seconds() for s in sleep_activities)
        hours_slept = total_sleep_seconds / 3600
        sleep_dates = sorted({s.activity.activity_date for s in sleep_activities}, reverse=True)
        daily_sleep_streak = 0
        expected_date = date.today()
        for d in sleep_dates:
            if d == expected_date:
                daily_sleep_streak += 1
                expected_date -= timedelta(days=1)
            elif d < expected_date:
                break

        # Goals
        goals_set = Goal.objects.filter(user=user).count()
        goals_completed = Goal.objects.filter(user=user, status='Completed').count()


    # dictionary for each user
        user_metrics.append({
            'username': user.username,
            'total_workouts': total_workouts,
            'distance_ran': distance_ran,
            'distance_swam': distance_swam,
            'distance_cycled': distance_cycled,
            'meals_tracked': meals_tracked,
            'lowest_carb_percentage': lowest_carb_percentage,
            'water_logs': water_logs,
            'amount_drank': amount_drank,
            'hours_slept': hours_slept,
            'daily_sleep_streak': daily_sleep_streak,
            'goals_set': goals_set,
            'goals_completed': goals_completed,
        })

    # building data structure for holding sorted lists for each metric ## dictionary->list->dictionary
    metric_names = [
        'total_workouts', 'distance_ran', 'distance_swam', 'distance_cycled',
        'meals_tracked', 'lowest_carb_percentage', 'water_logs', 'amount_drank',
        'hours_slept', 'daily_sleep_streak', 'goals_set', 'goals_completed'
    ]

    leaderboard = {} # master dictionary
    for metric in metric_names:
        # lower values are better for some metrics
        if metric == 'lowest_carb_percentage':
            sorted_users = sorted(user_metrics, key=lambda u: u[metric])
        else:
            sorted_users = sorted(user_metrics, key=lambda u: u[metric], reverse=True)

        ranking_list = [] # entries in master dictionary
        for rank, u in enumerate(sorted_users, start=1):
            ranking_list.append({
                'username': u['username'],
                'value': u[metric],
                'rank': rank
            }) # a dictionary entry in the ranked list
        leaderboard[metric] = ranking_list

    # cache for one day (86400 seconds).
    cache.set('leaderboard_metrics', leaderboard, 86400)
    return leaderboard
