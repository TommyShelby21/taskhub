from django.contrib.auth.models import User
from django.test import TestCase

from .models import AssignedTask, Task, Team, TeamMember, UserProfile


class TeamModelTests(TestCase):
    def test_create_team(self):
        team = Team.objects.create(name='Alfa')
        self.assertEqual(team.name, 'Alfa')


class TeamMemberModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='u1', password='pass12345')
        self.team = Team.objects.create(name='Alfa')

    def test_team_member_default_not_leader(self):
        member = TeamMember.objects.create(user=self.user, team=self.team)
        self.assertFalse(member.leader)

    def test_team_member_listed_under_team(self):
        TeamMember.objects.create(user=self.user, team=self.team)
        self.assertEqual(self.team.teammembers.count(), 1)


class UserProfileModelTests(TestCase):
    def test_user_profile_defaults_to_not_demo(self):
        user = User.objects.create_user(username='u1', password='pass12345')
        team = Team.objects.create(name='Alfa')
        profile = UserProfile.objects.create(user=user, selected_team=team)
        self.assertFalse(profile.demo)


class TaskModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='u1', password='pass12345')
        self.team = Team.objects.create(name='Alfa')

    def test_task_creation_defaults(self):
        task = Task.objects.create(
            name='Fix bug',
            team=self.team,
            created_by=self.user,
        )
        self.assertFalse(task.is_hidden)
        self.assertIsNotNone(task.created_at)

    def test_task_survives_creator_deletion(self):
        task = Task.objects.create(name='Fix bug', team=self.team, created_by=self.user)
        self.user.delete()
        task.refresh_from_db()
        self.assertIsNone(task.created_by)

    def test_task_deleted_with_team(self):
        task = Task.objects.create(name='Fix bug', team=self.team, created_by=self.user)
        self.team.delete()
        self.assertFalse(Task.objects.filter(id=task.id).exists())


class AssignedTaskModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='u1', password='pass12345')
        self.team = Team.objects.create(name='Alfa')
        self.task = Task.objects.create(name='Fix bug', team=self.team, created_by=self.user)

    def test_assigned_task_completed_default_false(self):
        assigned = AssignedTask.objects.create(task=self.task, team=self.team)
        self.assertFalse(assigned.completed)

    def test_assigned_task_deleted_with_task(self):
        assigned = AssignedTask.objects.create(task=self.task, team=self.team)
        self.task.delete()
        self.assertFalse(AssignedTask.objects.filter(id=assigned.id).exists())
