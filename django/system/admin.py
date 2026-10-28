from django.contrib import admin
from system.models import Team, Task, TeamMember, AssignedTask, UserProfile
# Register your models here.

admin.site.register(Team)
admin.site.register(Task)
admin.site.register(TeamMember)
admin.site.register(AssignedTask)
admin.site.register(UserProfile)
