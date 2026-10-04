from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from system.serializers import UserSerializer, TaskSerializer, AssignedTaskSerializer, TeamSerializer, UserProfileSerializer, TeamMemberSerializer
from system.models import Team, Task, TeamMember, AssignedTask, UserProfile
from django.contrib.auth.models import User


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def users(request):
    users = User.objects.all()

    serializer = UserSerializer(users, many=True)

    return Response({'items': serializer.data}, status=200)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user(request, user_id):
    user = User.objects.get(id=user_id)

    serializer = UserSerializer(user)

    return Response({'items': serializer.data}, status=200)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_profile(request, user_id):
    user = User.objects.get(id=user_id)

    profile = UserProfile.objects.get(user=user)

    serializer = UserProfileSerializer(profile)

    return Response({'user': serializer.data}, status=200)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def team_tasks(request, team_id):
    team = Team.objects.get(id=team_id)

    tasks = Task.objects.filter(team=team).order_by('name')

    serializer = TaskSerializer(tasks, many=True)

    return Response({'tasks': serializer.data}, status=200)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def team_members(request, team_id):
    team = Team.objects.get(id=team_id)

    members = TeamMember.objects.filter(team=team)

    serializer = TeamMemberSerializer(members, many=True)

    return Response({'members': serializer.data}, status=200)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def add_team_task(request, team_id):
    team = Team.objects.get(id=team_id)

    task_name = request.data.get('name')
    task_description = request.data.get('description', '')
    task_users = request.data.get('users', [])
    task_priority = request.data.get('priority', Task.PRIORITY_MEDIUM)

    if not task_name:
        return Response({'error': 'Task name is required'}, status=400)

    if task_priority not in dict(Task.PRIORITY_CHOICES):
        return Response({'error': 'Invalid priority'}, status=400)

    task = Task.objects.create(name=task_name, description=task_description, priority=task_priority, team=team, created_by=request.user)
    task.team_members.add(*task_users)

    return Response({'message': 'Task created successfully'}, status=201)


@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def update_team_task(request, team_id):
    team = Team.objects.get(id=team_id)

    task_id = request.data.get('taskId')
    task = Task.objects.get(id=task_id, team=team)

    task_name = request.data.get('name')
    task_description = request.data.get('description', '')
    task_priority = request.data.get('priority', task.priority)

    if not task_name:
        return Response({'error': 'Task name is required'}, status=400)

    if task_priority not in dict(Task.PRIORITY_CHOICES):
        return Response({'error': 'Invalid priority'}, status=400)

    task.name = task_name
    task.description = task_description
    task.priority = task_priority
    task.save()

    if 'users' in request.data:
        task.team_members.set(request.data.get('users') or [])

    serializer = TaskSerializer(task)

    return Response({'task': serializer.data}, status=200)


@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def delete_team_task(request, team_id):
    team = Team.objects.get(id=team_id)

    task_id = request.data.get("taskId")

    try:
        task = Task.objects.get(id=task_id, team=team)
    except Task.DoesNotExist:
        assigned_task = AssignedTask.objects.get(id=task_id, team=team)
        task = assigned_task.task

    task.is_hidden = True
    task.save()

    return Response({'message': 'Task hidden successfully'}, status=200)


@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def team_tasks_update(request, team_id):
    team = Team.objects.get(id=team_id)

    task_id = request.data.get('taskId')
    task = Task.objects.get(id=task_id)

    team_member_ids = request.data.get('teamMemberIds', [])

    defaults = {}
    if 'datetime' in request.data:
        defaults['datetime'] = request.data.get('datetime')
    if 'duration' in request.data:
        try:
            duration = int(request.data.get('duration'))
        except (TypeError, ValueError):
            return Response({'error': 'Invalid duration'}, status=400)
        if not 1 <= duration <= 24:
            return Response({'error': 'Duration must be between 1 and 24 hours'}, status=400)
        defaults['duration'] = duration

    assigned_task, created = AssignedTask.objects.update_or_create(task=task, team=team, defaults=defaults)

    return Response({'message': 'Task updated successfully'}, status=201)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def assign_task_to_members(request, team_id):
    team = Team.objects.get(id=team_id)

    task_id = request.data.get('taskId')
    task = Task.objects.get(id=task_id)

    members_ids = request.data.get('teamMembers', [])

    assigned_task, created = AssignedTask.objects.get_or_create(task=task, team=team)

    task.team_members.set(members_ids)

    return Response({'message': 'Task assigned successfully'}, status=201)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def team_assigned_tasks(request, team_id):
    team = Team.objects.get(id=team_id)

    tasks = AssignedTask.objects.filter(team=team)

    serializer = AssignedTaskSerializer(tasks, many=True)

    return Response({'assigned_tasks': serializer.data}, status=200)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def available_user_teams(request):
    user = request.user

    teams = Team.objects.filter(teammembers__user=user).distinct()

    serializer = TeamSerializer(teams, many=True)

    return Response({'teams': serializer.data}, status=200)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def add_team(request):
    user = request.user
    user_instance = User.objects.get(id=user.id)

    name = request.data.get('name')
    if not name:
        return Response({'error': 'Name required'}, status=400)

    team = Team.objects.create(name=name)
    leader = TeamMember.objects.create(user=user_instance, leader=True, team=team)

    return Response({'message': 'Team created successfully'}, status=201)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def set_user_profile(request):
    user = request.user

    team_id = request.data.get('team')

    team = Team.objects.get(id=team_id)

    user_profile, created = UserProfile.objects.get_or_create(user=user, selected_team=team)

    user_profile.selected_team = team
    user_profile.save()

    return Response({'message': 'User profile updated successfully'}, status=201)
