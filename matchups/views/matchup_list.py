from django.shortcuts import render
from matchups import model_utilities, utilities

def current_matchups(request):
    return weekly_matchups(request, utilities.current_week_number())

def weekly_matchups(request, week_number):
    if int(week_number) < 1:
        context = {'date_range' : 'Week number is invalid'}
        return render(request, 'matchup_list.html', context)
    matchup_list = model_utilities.matchups_for_week(week_number)
    date = str(utilities.game_day(week_number).strftime("%b %d, %Y"))
    context = {'matchup_list' : matchup_list,
               'date_range' : date,}
    return render(request, 'matchup_list.html', context)