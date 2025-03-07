# tests/test_models.py
import pytest
from django.contrib.auth.models import User
from LogMyFit.models import Activity


@pytest.mark.django_db
def test_create_activity():
    user = User.objects.create_user(username="testuser", password="password123")
    activity = Activity.objects.create(user=user, activityType="Workout")

    assert activity.user.username == "testuser"
    assert activity.activityType == "Workout"
