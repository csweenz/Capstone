# Create your tests here.
import pytest
from django.contrib.auth.models import User
from django.urls import reverse

from LogMyFit.forms import ActivityForm
from LogMyFit.models import Activity


@pytest.mark.django_db
def test_create_activity():
    user = User.objects.create_user(username="testuser", password="password123")
    activity = Activity.objects.create(user=user, activityType="Workout")

    assert activity.user.username == "testuser"
    assert activity.activityType == "Workout"



@pytest.mark.django_db
def test_dashboard_view(client):
    user = User.objects.create_user(username="testuser", password="password123")
    client.login(username="testuser", password="password123")

    response = client.get(reverse('dashboard'))
    assert response.status_code == 200


def test_activity_form_valid():
    form = ActivityForm(data={"activityType": "Workout"})
    assert form.is_valid()

def test_activity_form_invalid():
    form = ActivityForm(data={})  # Empty data
    assert not form.is_valid()