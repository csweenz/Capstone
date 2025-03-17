# tests/test_views.py
import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from LogMyFit.models import Activity, WorkoutActivity


@pytest.mark.django_db
def test_dashboard_view(client):
    User.objects.create_user(username="testuser", password="password123")
    client.login(username="testuser", password="password123")

    response = client.get(reverse('dashboard'))
    assert response.status_code == 200

@pytest.mark.django_db
def test_dashboard_logged_out_view(client):
    User.objects.create_user(username="testuser", password="password123")
    client.login(username="testuser", password="password123")
    client.logout()

    response = client.get(reverse('dashboard'))
    assert not response.status_code == 200

def test_dashboard_default_view(client):
    response = client.get(reverse('dashboard'))
    assert not response.status_code == 200


def test_home_view(client):

    response = client.get(reverse('home'))
    assert response.status_code == 200

def test_success_view(client):
    response = client.get(reverse('success'))
    assert response.status_code == 200

def test_add_user_view(client):
    response = client.get(reverse('add_user'))
    assert response.status_code == 200

def test_login_view(client):
    response = client.get(reverse('login'))
    assert response.status_code == 200


@pytest.mark.django_db
def test_edit_activity_view(client):
    user = User.objects.create_user(username="testuser", password="password123")
    client.login(username='testuser', password='password123')
    activity = Activity.objects.create(activityID=1, user=user, activityType='Workout')
    WorkoutActivity.objects.create(activity=activity)
    response = client.get(reverse('edit_activity', kwargs={'activity_id': activity.activityID}))
    assert response.status_code == 200

def delete_activity_view(client):
    response = client.get(reverse('delete_activity'))
    assert response.status_code == 404

@pytest.mark.django_db
def test_user_list_view(client):
    response = client.get(reverse('user_list'))
    assert response.status_code == 200