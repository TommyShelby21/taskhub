from django.contrib import admin
from django.urls import path, include
from system.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', users, name='users'),
    path('user/<int:user_id>/', user_detail, name='user_detail'),
    path('profile/', profile, name='profile'),
    path('profile/set_user_profile/', set_user_profile, name='set_user_profile'),
    path('available_user_teams/', available_user_teams, name='available_user_teams'),
    path('team/add', add_team, name='add_team'),
    path('team/<int:team_id>/members/', team_members, name='team_members'),
    path('team/<int:team_id>/tasks/', team_tasks, name='team_tasks'),
    path('team/<int:team_id>/tasks/assign', assign_task_to_members, name='assign_task_to_members'),
    path('team/<int:team_id>/tasks/add/', add_team_task, name='add_team_task'),
    path('team/<int:team_id>/task/delete/', delete_team_task, name='delete_team_task'),
    path('team/<int:team_id>/tasks/update/', team_tasks_update, name='team_tasks_update'),
    path('team/<int:team_id>/assigned_tasks/', team_assigned_tasks, name='team_assigned_tasks'),
]
