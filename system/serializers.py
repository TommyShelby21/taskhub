from rest_framework import serializers
from django.contrib.auth.models import User
from system.models import Task, AssignedTask, Team, UserProfile, TeamMember


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False)

    class Meta:
        model = UserProfile
        fields = '__all__'

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = '__all__'


class TeamMemberSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False)
    class Meta:
        model = TeamMember
        fields = '__all__'


class AssignedTaskSerializer(serializers.ModelSerializer):
    datetime = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%SZ")
    task = TaskSerializer(many=False)
    class Meta:
        model = AssignedTask
        fields = '__all__'
