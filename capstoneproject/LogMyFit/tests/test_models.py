# tests/test_models.py
import pytest
from django.contrib.auth.models import User
from LogMyFit.models import Activity, Goal, Leaderboard
from datetime import date


@pytest.mark.django_db
def test_create_activity():
    user = User.objects.create_user(username="testuser", password="password123")
    activity = Activity.objects.create(user=user, activityType="Workout")

    assert activity.user.username == "testuser"
    assert activity.activityType == "Workout"

@pytest.mark.django_db
def test_create_goal():
    user = User.objects.create_user(username="testuser", password="password123")
    goal = Goal.objects.create(user=user, goalType="Nutrition", targetValue=100, targetDate=date.today())

    assert goal.user.username == "testuser"
    assert goal.goalType == "Nutrition"

@pytest.mark.django_db
def test_create_leaderboard_entry():
    user = User.objects.create_user(username="testuser", password="password123")
    leaderboard = Leaderboard.objects.create(user=user, startDate=date.today(), endDate=date.today())

    assert leaderboard.user.username == "testuser"