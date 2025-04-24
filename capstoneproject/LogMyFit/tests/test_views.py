# tests/test_views.py
import pytest
from django.contrib.auth.models import User
from django.core.cache import cache
from django.urls import reverse
from LogMyFit.models import Activity, WorkoutActivity, Goal, FitnessGoal, UserProfile, ChatboxMessage
from capstoneproject.utils.create_leaderboard_metrics import create_leaderboard_metrics


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


@pytest.mark.django_db
def test_dashboard_full_view(client):
    user = User.objects.create_user(username="testuser", password="password123")
    client.login(username="testuser", password="password123")
    activity = Activity.objects.create(activityID=1, user=user, activityType='Workout')
    WorkoutActivity.objects.create(activity=activity)
    cache.delete('activities_testuser_30_days')
    response = client.get(reverse('dashboard'))
    visualization_data = response.context.get('visualization_data')
    chart_data_json = response.context.get('chart_data_json')
    assert visualization_data is not None
    assert visualization_data['total_workout_activities'] == 1
    assert chart_data_json is not None


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
def test_edit_goal_view(client):
    user = User.objects.create_user(username='testuser', password='password123')
    client.login(username='testuser', password='password123')
    goal = Goal.objects.create(goalID=1, user=user, goalType='Fitness')
    FitnessGoal.objects.create(goal=goal)
    response = client.get(reverse('edit_goal', kwargs={'goal_id': goal.goalID}))
    assert response.status_code == 200


@pytest.mark.django_db
def test_user_list_view(client):
    response = client.get(reverse('user_list'))
    assert response.status_code == 200


@pytest.mark.django_db
def test_leaderboards_view():
    user = User.objects.create_user(username="testuser", password="password123")
    user2 = User.objects.create_user(username="testuser2", password="password123")
    activity = Activity.objects.create(activityID=1, user=user, activityType='Workout')
    activity2 = Activity.objects.create(activityID=2, user=user, activityType='Workout')
    activity3 = Activity.objects.create(activityID=3, user=user2, activityType='Workout')
    WorkoutActivity.objects.create(activity=activity)
    WorkoutActivity.objects.create(activity=activity2)
    WorkoutActivity.objects.create(activity=activity3)
    leaderboards_metrics = create_leaderboard_metrics()
    assert leaderboards_metrics is not None
    assert leaderboards_metrics['total_workouts'][0]['username'] == 'testuser'


@pytest.mark.django_db
def test_clear_leaderboard_cache_view(client):
    User.objects.create_user(username="testuser", password="password123")
    client.login(username="testuser", password="password123")
    cache.set('leaderboard_metrics', {'test': 'data'}, 86400)
    url = reverse('clear_leaderboard_cache')
    response = client.get(url)
    assert cache.get('leaderboard_metrics') is None
    assert response.status_code == 302
    assert 'leaderboards' in response.url


@pytest.mark.django_db
def test_profile_view_public(client):
    owner = User.objects.create_user(username="owner", password="password123", email="owner@example.com")
    User.objects.create_user(username="viewer", password="password123", email="viewer@example.com")
    client.login(username="viewer", password="password123")
    # viewer requests owner's profile.
    url = reverse('profile', kwargs={'username': owner.username})
    response = client.get(url)
    context = response.context
    assert response.status_code == 200
    assert context.get('is_owner') is False
    assert context.get('profile_user').username == owner.username


@pytest.mark.django_db
def test_profile_view_private(client):
    user = User.objects.create_user(username="testuser", password="password123", email="test@example.com")
    client.login(username="testuser", password="password123")
    url = reverse('profile', kwargs={'username': user.username})
    response = client.get(url)
    context = response.context
    assert response.status_code == 200
    assert context.get('is_owner') is True
    assert context.get('profile_user').username == user.username


@pytest.mark.django_db
def test_update_theme_view(client):
    user = User.objects.create_user(username="testuser", password="password123", email="test@example.com")
    client.login(username="testuser", password="password123")
    UserProfile.objects.get_or_create(user=user)
    url = reverse('update_theme')
    data = {'preferred_theme': 'maximal'}
    response = client.post(url, data)
    profile = UserProfile.objects.get(user=user)
    assert response.status_code == 302
    assert profile.preferred_theme == 'maximal'


@pytest.mark.django_db
def test_post_chat_view(client):
    sender = User.objects.create_user(username="sender", password="password123")
    recipient = User.objects.create_user(username="recipient", password="password123")
    client.login(username="sender", password="password123")
    url = reverse('post_chat')
    data = {
        'message': 'Test to recipient',
        'recipient': str(recipient.id)
    }
    response = client.post(url, data)
    assert response.status_code == 200
    json_data = response.json()
    assert json_data.get('status') == 'ok'
    messages = ChatboxMessage.objects.filter(recipient=recipient, sender=sender, message='Test to recipient')
    assert messages.count() == 1


@pytest.mark.django_db
def test_get_chats_view(client):
    sender = User.objects.create_user(username="sender", password="password123")
    recipient = User.objects.create_user(username="recipient", password="password123")
    ChatboxMessage.objects.create(sender=sender, recipient=recipient, message="Test message")
    client.login(username="recipient", password="password123")
    url = reverse('get_chats') + f'?recipient={recipient.id}'
    response = client.get(url)
    json_data = response.json()
    assert response.status_code == 200
    assert 'messages' in json_data
    assert len(json_data['messages']) >= 1
