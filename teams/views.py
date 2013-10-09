from django.shortcuts import render
from teams.models import Team

def team_manager(request):
    team_list = Team.objects.all()
    context = {'team_list': team_list}
    return render(request, 'teammanager.html', context)