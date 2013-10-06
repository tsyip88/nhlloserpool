from django.shortcuts import render
from django.contrib.auth.decorators import permission_required
from matchups import utilities
from matchups.models import PickSet 
from django.db.models import Count
    
@permission_required('matchups.add_matchup')
def admin_scoreboard_for_week(request, week_number):
    return scoreboard(request, week_number, True)

def scoreboard_current_week(request):
    return scoreboard(request, utilities.current_week_number())
    
def scoreboard(request, week_number, is_admin=False):
    pick_sets = order_list(request.user)
    max_number_of_picks = max(PickSet.objects.annotate(Count('pick')).values_list('pick__count', flat=True))
    week_date = str(utilities.game_day(week_number).strftime("%b %d, %Y"))
    hide_other_team_picks_for_current_week = not utilities.has_first_matchup_of_week_started(week_number)
    context = {'pick_sets' : pick_sets,
               'max_weeks': max_number_of_picks,
               'selected_week': int(week_number),
               'week_date': week_date,
               'hide_other_team_picks_for_current_week': hide_other_team_picks_for_current_week,
               'is_admin': is_admin}
    return render(request, 'scoreboard.html', context)

def order_list(current_user):
    ordered_list = list()
    pick_sets = PickSet.objects.order_by('user')
    index_to_insert = 0
    for pick_set in pick_sets:
        if pick_set.user == current_user:
            ordered_list.insert(index_to_insert,pick_set)
            index_to_insert += 1
        else:
            ordered_list.append(pick_set)
    return ordered_list