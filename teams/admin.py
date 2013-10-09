from django.contrib import admin
from teams.models import League, Conference, Division, Team

admin.site.register(League)
admin.site.register(Conference)
admin.site.register(Division)
admin.site.register(Team)