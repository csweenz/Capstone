from datetime import datetime

from django.contrib.auth.models import User
from django.core.cache import cache
from LogMyFit.models import Goal, ChatboxMessage


def check_all_goals(user):
    system_user = User.objects.get_or_create(username="System")
    active_goals = Goal.objects.filter(user=user, status="Active")

    for goal in active_goals:
        if goal.targetDate < datetime.today().date():
            goal.status = "Failed"
            goal.save(update_fields=["status"])
            continue

        if goal.goalType == "Fitness":
            fields = {
                "targetWeightLifted": goal.fitness_goal.targetWeightLifted or 0,
                "targetDistance": goal.fitness_goal.targetDistance or 0,
                "targetDuration": goal.fitness_goal.targetDuration or 0,
            }
            progress = aggregate_fitness_progress(user, goal, goal.fitness_goal)

        elif goal.goalType == "Nutrition":
            fields = {
                "dailyCalorieIntake": goal.nutrition_goal.dailyCalorieIntake or 0,
                "proteinGoal": goal.nutrition_goal.proteinGoal or 0,
                "sugarLimit": goal.nutrition_goal.sugarLimit or 0,
            }
            progress = aggregate_nutrition_progress(user, goal, goal.nutrition_goal)

        elif goal.goalType == "Water":
            fields = {
                "dailyWaterIntakeTarget": goal.water_goal.dailyWaterIntakeTarget or 0
            }
            progress = aggregate_water_progress(user, goal)

        elif goal.goalType == "Sleep":
            fields = {
                "targetHours": goal.sleep_goal.targetHours or 0
            }
            progress = aggregate_sleep_progress(user, goal)

        else:
            continue

        # pick the field with max threshold to set goal entry's targetType
        target_value = fields[max(fields, key=fields.get)]
        goal.targetType = max(fields, key=fields.get)

        if target_value > 0:
            goal.progress_percentage = int((progress / target_value) * 100)
        else:
            goal.progress_percentage = 0

        if progress >= target_value:
            goal.status = "Completed"
            ChatboxMessage.objects.create(
                sender=system_user,
                recipient=None,
                message=(str(goal) + " completed successfully!"),
                is_system=True,
                is_admin=False,
                is_announcement=True,
            )
        goal.save(update_fields=["targetType", "progress_percentage", "status"])
        cache.delete(f'goals_{user}')
        cache.delete(f"chat_messages_{user}")


def aggregate_fitness_progress(user, goal, fitness_goal):
    total_weight = 0
    total_distance = 0
    total_duration = 0
    activities = user.activity_set.filter(activityType='workout', dateLogged__date__range=[goal.created_at, datetime.today().date()])
    for activity in activities:
        if fitness_goal.targetWeightLifted:
            total_weight += activity.fitness_goal.weight_lifted
        if fitness_goal.targetDistance:
            total_distance += activity.fitness_goal.distance
        if fitness_goal.targetDuration:
            total_duration += activity.fitness_goal.duration
    return max(total_weight, total_distance, total_duration)


def aggregate_nutrition_progress(user, goal, nutrition_goal):
    total_calories = 0
    total_protein = 0
    total_carbs = 0
    activities = user.activity_set.filter(activityType='meal', dateLogged__date__range=[goal.created_at, datetime.today().date()])
    for activity in activities:
        if nutrition_goal.dailyCalorieIntake is not None:
            total_calories += activity.nutrition_goal.calories
        if nutrition_goal.proteinGoal is not None:
            total_protein += activity.nutrition_goal.protein
        if nutrition_goal.sugarLimit is not None:
            total_carbs += activity.nutrition_goal.carbs
    return max(total_calories, total_protein, total_carbs)


def aggregate_water_progress(user, goal):
    total_water = 0
    activities = user.activity_set.filter(activityType='water', dateLogged__date__range=[goal.created_at, datetime.today().date()])
    for activity in activities:
        total_water += activity.water_activity.amount
    return total_water


def aggregate_sleep_progress(user, goal):
    total_sleep = 0
    activities = user.activity_set.filter(activityType='sleep', dateLogged__date__range=[goal.created_at, datetime.today().date()])
    for activity in activities:
        total_sleep += activity.sleep_activity.duration
    return total_sleep


def check_goals_on_new_activity(activity):
    user = activity.user
    system_user = User.objects.get(username="System")
    # compute new activity contribution
    if activity.activityType == "Workout":
        for goal in Goal.objects.filter(user=user, status='Active', goalType='Fitness'):
            wa = activity.workout_activity
            contrib = max(
                    wa.weightLifted or 0,
                    wa.distance or 0,
                    wa.duration or 0,
            )
            fields = {
                "targetWeightLifted": goal.fitness_goal.targetWeightLifted or 0,
                "targetDistance": goal.fitness_goal.targetDistance or 0,
                "targetDuration": goal.fitness_goal.targetDuration or 0,
            }
            threshold = fields[max(fields, key=fields.get)]
            goal.targetType = max(fields, key=fields.get)
            progress_value = ((goal.progress_percentage * threshold) / 100 or 0) + contrib
            if progress_value / threshold > 1:
                progress_value = threshold
            goal.progress_percentage = int((progress_value / threshold) * 100) if threshold > 0 else 0
            if progress_value >= threshold:
                goal.status = "Completed"
                ChatboxMessage.objects.create(
                    sender=system_user,
                    recipient=None,  # broadcast
                    message=(str(goal) + " completed successfully!"),
                    is_system=True,
                    is_admin=False,
                    is_announcement=True,
                )
            goal.save(update_fields=["targetType", "progress_percentage", "status"])
            cache.delete(f'goals_{user}')
            cache.delete(f"chat_messages_{user}")
    elif activity.activityType == "Meal":
        for goal in Goal.objects.filter(user=user, status='Active', goalType='Nutrition'):
            ma = activity.meal_activity
            contrib = max(
                    ma.calories or 0,
                    ma.protein or 0,
                    ma.carbs or 0
            )
            fields = {
                "dailyCalorieIntake": goal.nutrition_goal.dailyCalorieIntake or 0,
                "proteinGoal": goal.nutrition_goal.proteinGoal or 0,
                "sugarLimit": goal.nutrition_goal.sugarLimit or 0,
            }
            threshold = fields[max(fields, key=fields.get)]
            goal.targetType = max(fields, key=fields.get)
            progress_value = ((goal.progress_percentage * threshold) / 100 or 0) + contrib
            if progress_value / threshold > 1:
                progress_value = threshold
            goal.progress_percentage = int((progress_value / threshold) * 100) if threshold > 0 else 0
            if progress_value >= threshold:
                goal.status = "Completed"
                ChatboxMessage.objects.create(
                    sender=system_user,
                    recipient=None,  # broadcast
                    message=(str(goal) + " completed successfully!"),
                    is_system=True,
                    is_admin=False,
                    is_announcement=True,
                )
            goal.save(update_fields=["targetType", "progress_percentage", "status"])
            cache.delete(f'goals_{user}')
            cache.delete(f"chat_messages_{user}")
    elif activity.activityType == "Water":
        for goal in Goal.objects.filter(user=user, status='Active', goalType='Water'):
            contrib = activity.water_activity.amount or 0
            threshold = goal.water_goal.dailyWaterIntakeTarget
            goal.targetType = 'dailyWaterIntakeTarget'
            progress_value = ((goal.progress_percentage * threshold) / 100 or 0) + contrib
            if progress_value / threshold > 1:
                progress_value = threshold
            if threshold > 0:
                goal.progress_percentage = int((progress_value / threshold) * 100)
            else:
                goal.progress_percentage = 0
            if progress_value >= threshold:
                goal.status = "Completed"
                ChatboxMessage.objects.create(
                    sender=system_user,
                    recipient=None,  # broadcast
                    message=(str(goal) + " completed successfully!"),
                    is_system=True,
                    is_admin=False,
                    is_announcement=True,
                )
            goal.save(update_fields=["targetType", "progress_percentage", "status"])
            cache.delete(f'goals_{user}')
            cache.delete(f"chat_messages_{user}")
    elif activity.activityType == "Sleep":
        for goal in Goal.objects.filter(user=user, status='Active', goalType='Sleep'):
            sa = activity.sleep_activity
            contrib = sa.duration.total_seconds() / 3600.0  # hours
            threshold = goal.sleep_goal.targetHours or 0
            goal.targetType = 'targetHours'
            progress_value = ((goal.progress_percentage * threshold) / 100 or 0) + contrib
            if progress_value / threshold > 1:
                progress_value = threshold
            if threshold > 0:
                goal.progress_percentage = int((progress_value / threshold) * 100)
            else:
                goal.progress_percentage = 0

            if progress_value >= threshold:
                goal.status = "Completed"
                ChatboxMessage.objects.create(
                    sender=system_user,
                    recipient=None,  # broadcast
                    message=(str(goal) + " completed successfully!"),
                    is_system=True,
                    is_admin=False,
                    is_announcement=True,
                )
            goal.save(update_fields=["targetType", "progress_percentage", "status"])
            cache.delete(f'goals_{user}')
            cache.delete(f"chat_messages_{user}")
