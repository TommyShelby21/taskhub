from django.db import models
from django.contrib.auth.models import User


class Team(models.Model):
    name = models.CharField(max_length=256, null=True, blank=True)


class UserProfile(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE, related_name='userprofile')
    selected_team = models.ForeignKey(Team, null=True, blank=True, on_delete=models.CASCADE)
    demo = models.BooleanField(default=False)


class TeamMember(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    leader = models.BooleanField(default=False)
    team = models.ForeignKey(Team, null=True, blank=True, on_delete=models.CASCADE, related_name='teammembers')


class Task(models.Model):
    PRIORITY_LOW = 'low'
    PRIORITY_MEDIUM = 'medium'
    PRIORITY_HIGH = 'high'
    PRIORITY_CHOICES = [
        (PRIORITY_LOW, 'Nízká'),
        (PRIORITY_MEDIUM, 'Střední'),
        (PRIORITY_HIGH, 'Vysoká'),
    ]

    name = models.CharField(max_length=128, null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    team = models.ForeignKey(Team, null=True, blank=True, on_delete=models.CASCADE)
    team_members = models.ManyToManyField(TeamMember, null=True, blank=True)
    is_hidden = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='created_tasks')
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default=PRIORITY_MEDIUM)


class AssignedTask(models.Model):
    task = models.ForeignKey(Task, null=True, blank=True, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, null=True, blank=True, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    datetime = models.DateTimeField(auto_now_add=False, null=True, blank=True)
    duration = models.PositiveSmallIntegerField(default=1)
