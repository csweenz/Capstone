# tests/test_forms.py
import datetime
import pytest
import LogMyFit.forms as forms


def test_activity_form_valid():
    form = forms.ActivityForm(data={"activityType": "Workout"})
    assert form.is_valid()


def test_activity_form_invalid():
    form = forms.ActivityForm(data={})  # Empty data
    assert not form.is_valid()


def test_workout_activity_form_valid():
    form = forms.WorkoutActivityForm(data={"exerciseType": "Running"})
    assert form.is_valid()


def test_workout_activity_form_invalid():
    form = forms.WorkoutActivityForm(data={})  # Empty data
    assert not form.is_valid()


def test_meal_activity_form_valid():
    form = forms.MealActivityForm(data={"calories": 100, "protein":0, "carbs":0, "fat":0, "mealType": "Breakfast"})
    assert form.is_valid()


def test_meal_activity_form_invalid():
    form = forms.MealActivityForm(data={})  # Empty data
    assert not form.is_valid()


def test_water_activity_form_valid():
    form = forms.WaterActivityForm(data={"amount": 100})
    assert form.is_valid()


def test_water_activity_form_invalid():
    form = forms.WaterActivityForm(data={})  # Empty data
    assert not form.is_valid()


def test_sleep_activity_form_valid():
    form = forms.SleepActivityForm(data={"duration": 0, "bedtime":datetime.datetime.now().time(), "wakeTime":datetime.datetime.now().time()})
    assert form.is_valid()


def test_sleep_activity_form_invalid():
    form = forms.SleepActivityForm(data={})  # Empty data
    assert not form.is_valid()

def test_theme_form_valid():
    form = forms.ThemeForm(data={'preferred_theme': 'minimal'})
    assert form.is_valid()

def test_theme_form_invalid():
    form = forms.ThemeForm(data={})
    assert not form.is_valid()

def test_fitness_goal_form_valid():
    form = forms.FitnessGoalForm(data={'targetDate' : 7, 'targetWeightLifted': 1})
    assert form.is_valid()

def test_fitness_goal_form_invalid():
    form = forms.FitnessGoalForm(data={})
    assert not form.is_valid()


def test_nutrition_goal_form_valid():
    form = forms.NutritionGoalForm(data={'targetDate' : 7, 'dailyCalorieIntake': 1})
    assert form.is_valid()


def test_nutrition_goal_form_invalid():
    form = forms.NutritionGoalForm(data={})
    assert not form.is_valid()


def test_water_goal_form_valid():
    form = forms.WaterGoalForm(data={'targetDate' : 7, 'dailyWaterIntakeTarget': 1})
    assert form.is_valid()


def test_water_goal_form_invalid():
    form = forms.WaterGoalForm(data={})
    assert not form.is_valid()


def test_sleep_goal_form_valid():
    form = forms.SleepGoalForm(data={'targetDate' : 7, 'targetHours': 1})
    assert form.is_valid()


def test_sleep_goal_form_invalid():
    form = forms.SleepGoalForm(data={})
    assert not form.is_valid()