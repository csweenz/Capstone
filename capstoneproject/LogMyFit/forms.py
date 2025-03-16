from datetime import date

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from LogMyFit.models import Activity, WorkoutActivity, MealActivity, WaterActivity, SleepActivity
from LogMyFit.models import Goal, FitnessGoal, NutritionGoal, WaterGoal, SleepGoal
from django import forms
from .models import Activity


class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class ActivityForm(forms.ModelForm):
    activity_date = forms.DateField(
        required=False,  # Allow it to be optional
        widget=forms.DateInput(attrs={'type': 'date'}),  # Use a date picker
        initial=date.today()  # Default to today's date
    )

    class Meta:
        model = Activity
        fields = ['activityType', 'activity_date']

# Workout Activity Form
class WorkoutActivityForm(forms.ModelForm):
    class Meta:
        model = WorkoutActivity
        fields = ['exerciseType', 'duration', 'distance', 'weightLifted', 'reps', 'sets']

# Meal Activity Form
class MealActivityForm(forms.ModelForm):
    class Meta:
        model = MealActivity
        fields = ['calories', 'protein', 'carbs', 'fat', 'mealType']

# Water Activity Form
class WaterActivityForm(forms.ModelForm):
    class Meta:
        model = WaterActivity
        fields = ['amount']

# Sleep Activity Form
class SleepActivityForm(forms.ModelForm):
    class Meta:
        model = SleepActivity
        fields = ['duration', 'bedtime', 'wakeTime']

# Fitness Goal Form
class FitnessGoalForm(forms.ModelForm):
    class Meta:
        model = FitnessGoal
        fields = ['targetWeightLifted', 'targetDistance', 'targetDuration']

# Nutrition Goal Form
class NutritionGoalForm(forms.ModelForm):
    class Meta:
        model = NutritionGoal
        fields = ['dailyCalorieIntake', 'proteinGoal', 'sugarLimit']

# Water Goal Form
class WaterGoalForm(forms.ModelForm):
    class Meta:
        model = WaterGoal
        fields = ['dailyWaterIntakeTarget']

# Sleep Goal Form
class SleepGoalForm(forms.ModelForm):
    class Meta:
        model = SleepGoal
        fields = ['targetHours']