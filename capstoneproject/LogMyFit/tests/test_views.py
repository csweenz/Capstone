# tests/test_views.py
import pytest
from django.contrib.auth.models import User
from django.urls import reverse


@pytest.mark.django_db
def test_dashboard_view(client):
    user = User.objects.create_user(username="testuser", password="password123")
    client.login(username="testuser", password="password123")

    response = client.get(reverse('dashboard'))
    assert response.status_code == 200
