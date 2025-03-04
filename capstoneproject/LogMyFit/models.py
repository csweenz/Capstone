from datetime import date
from django.contrib.auth.models import User
from django.db import models


# Activity Model
class Activity(models.Model):
    ACTIVITY_TYPES = [
        ('Workout', 'Workout'),
        ('Meal', 'Meal'),
        ('Water', 'Water'),
        ('Sleep', 'Sleep')
    ]

    activityID = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    activityType = models.CharField(max_length=10, choices=ACTIVITY_TYPES)
    dateLogged = models.DateTimeField(auto_now_add=True)
    activity_date = models.DateField(default=date.today)

    def __str__(self):
        return f"{self.user.username} - {self.activityType} on {self.dateLogged}"


# Workout Activity Model
class WorkoutActivity(models.Model):
    EXERCISE_TYPES = [
        ('Running', 'Running'),
        ('Weightlifting', 'Weightlifting'),
        ('Cycling', 'Cycling'),
        ('Swimming', 'Swimming'),
        ('Other', 'Other')
    ]

    activity = models.OneToOneField(Activity, on_delete=models.CASCADE, primary_key=True, related_name='workout_activity')
    exerciseType = models.CharField(max_length=20, choices=EXERCISE_TYPES)

    duration = models.FloatField(null=True, blank=True)
    distance = models.FloatField(null=True, blank=True)
    weightLifted = models.FloatField(null=True, blank=True)
    reps = models.IntegerField(null=True, blank=True)
    sets = models.IntegerField(null=True, blank=True)


# Meal Activity Model
class MealActivity(models.Model):
    MEAL_TYPES = [
        ('Breakfast', 'Breakfast'),
        ('Lunch', 'Lunch'),
        ('Dinner', 'Dinner'),
        ('Snack', 'Snack')
    ]

    activity = models.OneToOneField(Activity, on_delete=models.CASCADE, primary_key=True, related_name='meal_activity')
    calories = models.FloatField()
    protein = models.FloatField(default=0)
    carbs = models.FloatField(default=0)
    fat = models.FloatField(default=0)
    mealType = models.CharField(max_length=10, choices=MEAL_TYPES)


# Water Activity Model
class WaterActivity(models.Model):
    activity = models.OneToOneField(Activity, on_delete=models.CASCADE, primary_key=True, related_name='water_activity')
    amount = models.FloatField()


# Sleep Activity Model
class SleepActivity(models.Model):
    activity = models.OneToOneField(Activity, on_delete=models.CASCADE, primary_key=True, related_name='sleep_activity')
    duration = models.FloatField()
    bedtime = models.TimeField()
    wakeTime = models.TimeField()


# Goal Model
class Goal(models.Model):
    GOAL_TYPES = [
        ('Fitness', 'Fitness'),
        ('Nutrition', 'Nutrition'),
        ('Sleep', 'Sleep'),
        ('Water', 'Water')
    ]

    STATUS_TYPES = [
        ('Active', 'Active'),
        ('Completed', 'Completed'),
        ('Failed', 'Failed')
    ]

    goalID = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="goals")
    goalType = models.CharField(max_length=10, choices=GOAL_TYPES)
    targetValue = models.FloatField()
    targetDate = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_TYPES, default="Active")

    def __str__(self):
        return f"{self.user.username} - {self.goalType} Goal"


# Fitness Goal Model
class FitnessGoal(models.Model):
    goal = models.OneToOneField(Goal, on_delete=models.CASCADE, primary_key=True)
    targetWeightLifted = models.FloatField(null=True, blank=True)
    targetDistance = models.FloatField(null=True, blank=True)
    targetDuration = models.FloatField(null=True, blank=True)


    def __str__(self):
        return f"Fitness Goal - {self.goal.goalType} ({self.goal.user.username})"


# Nutrition Goal Model
class NutritionGoal(models.Model):
    goal = models.OneToOneField(Goal, on_delete=models.CASCADE, primary_key=True)
    dailyCalorieIntake = models.FloatField(null=True, blank=True)
    proteinGoal = models.FloatField(null=True, blank=True)
    sugarLimit = models.FloatField(null=True, blank=True)

# Water Goal Model
class WaterGoal(models.Model):
    goal = models.OneToOneField(Goal, on_delete=models.CASCADE, primary_key=True)
    dailyWaterIntakeTarget = models.FloatField(default=0)


# Sleep Goal Model
class SleepGoal(models.Model):
    goal = models.OneToOneField(Goal, on_delete=models.CASCADE, primary_key=True)
    targetHours = models.FloatField(default=0)


# Leaderboard Model
class Leaderboard(models.Model):
    leaderboardID = models.AutoField(primary_key=True)
    challengeName = models.CharField(max_length=255)
    startDate = models.DateField()
    endDate = models.DateField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="leaderboard_entries")
    rank = models.IntegerField(null=True, blank=True)
    score = models.FloatField(default=0)

    def __str__(self):
        return f"{self.challengeName} - {self.user.username} (Rank: {self.rank})"
