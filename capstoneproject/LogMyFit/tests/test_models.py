# tests/test_models.py
import pytest
from django.contrib.auth.models import User

from LogMyFit.models import Activity, Goal, Leaderboard, ChatboxMessage, UserProfile
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
    goal = Goal.objects.create(user=user, goalType="Nutrition", targetDate=date.today())
    assert goal.user.username == "testuser"
    assert goal.goalType == "Nutrition"


@pytest.mark.django_db
def test_create_leaderboard_entry():
    user = User.objects.create_user(username="testuser", password="password123")
    leaderboard = Leaderboard.objects.create(user=user, startDate=date.today(), endDate=date.today())

    assert leaderboard.user.username == "testuser"


@pytest.mark.django_db
def test_get_user_profile(client):
    user = User.objects.create_user(username="testuser", password="password123")
    UserProfile.objects.get_or_create(user=user)
    assert user.profile.preferred_theme == 'minimal'


@pytest.mark.django_db
def test_chatbox_message():
    sender = User.objects.create_user(username="testuser", password="password123")
    recipient = User.objects.create_user(username="testuser2", password="password123")
    message = ChatboxMessage.objects.create(sender=sender, recipient=recipient)
    assert message.recipient.username == "testuser2"
