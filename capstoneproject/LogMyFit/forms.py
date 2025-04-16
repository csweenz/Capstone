from datetime import date

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from LogMyFit.models import Activity, WorkoutActivity, MealActivity, WaterActivity, SleepActivity
from LogMyFit.models import Goal, FitnessGoal, NutritionGoal, WaterGoal, SleepGoal, UserProfile
from django import forms
from .models import Activity


class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class ThemeForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['preferred_theme']

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
    bedtime = forms.TimeField(
        widget=forms.TimeInput(format='%H:%M', attrs={'type': 'time'}),
        input_formats=['%H:%M'],
    )
    wakeTime = forms.TimeField(
        widget=forms.TimeInput(format='%H:%M', attrs={'type': 'time'}),
        input_formats=['%H:%M'],
    )
    class Meta:
        model = SleepActivity
        fields = ['bedtime', 'wakeTime']

# Fitness Goal Form
class FitnessGoalForm(forms.ModelForm):
    targetDate = forms.FloatField(
        label="Days Until Deadline", #label and help_text would make inputs more clear
        initial=7
    )
    class Meta():
        model = FitnessGoal
        fields = ['targetWeightLifted', 'targetDistance', 'targetDuration', 'targetDate']

# Nutrition Goal Form
class NutritionGoalForm(forms.ModelForm):
    targetDate = forms.FloatField(
        label="Days Until Deadline",
        initial=7
    )
    class Meta:
        model = NutritionGoal
        fields = ['dailyCalorieIntake', 'proteinGoal', 'sugarLimit']

# Water Goal Form
class WaterGoalForm(forms.ModelForm):
    targetDate = forms.FloatField(
        label="Days Until Deadline",
        initial=7
    )
    class Meta:
        model = WaterGoal
        fields = ['dailyWaterIntakeTarget']

# Sleep Goal Form
class SleepGoalForm(forms.ModelForm):
    targetDate = forms.FloatField(
        label="Days Until Deadline",
        initial=7
    )
    class Meta:
        model = SleepGoal
        fields = ['targetHours']