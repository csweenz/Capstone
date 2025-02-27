from django.db import models
from django.contrib.auth.models import User

class Activity(models.Model):
    TYPE_CHOICES = [
        ('Workout', 'Workout'),
        ('Meal', 'Meal'),
        ('Water', 'Water'),
        ('Sleep', 'Sleep'),
    ]

    activityID = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    date_logged = models.DateField(auto_now_add=True)
    activity_date = models.DateField(null=True, blank=True)
    duration = models.FloatField(null=True, blank=True)
    amount = models.FloatField(null=True, blank=True)

    class Meta:
        db_table = 'activity'

    def __str__(self):
        return f"{self.user.username} - {self.type} ({self.date_logged})"
