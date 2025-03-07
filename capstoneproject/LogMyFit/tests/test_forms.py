# tests/test_forms.py
import pytest
from LogMyFit.forms import ActivityForm


def test_activity_form_valid():
    form = ActivityForm(data={"activityType": "Workout"})
    assert form.is_valid()


def test_activity_form_invalid():
    form = ActivityForm(data={})  # Empty data
    assert not form.is_valid()
