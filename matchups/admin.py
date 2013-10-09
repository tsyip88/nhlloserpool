from django.contrib import admin
from matchups.models import Matchup, Pick, PickSet

admin.site.register(Matchup)
admin.site.register(Pick)
admin.site.register(PickSet)