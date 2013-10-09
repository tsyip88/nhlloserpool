from django.shortcuts import render
from django.contrib.auth.decorators import permission_required
from matchups import utilities
from matchups.models import PickSet 
    
@permission_required('matchups.add_matchup')
def admin_scoreboard_for_week(request, week_number):
    return scoreboard(request, week_number, True)

def scoreboard_current_week(request):
    return scoreboard(request, utilities.current_week_number())
    
def scoreboard(request, week_number, is_admin=False):
    pick_sets = order_list(request.user)
    weeks = range(1,utilities.current_week_number()+1)
    week_date = str(utilities.game_day(week_number).strftime("%b %d, %Y"))
    context = {'pick_sets' : pick_sets,
               'weeks': weeks,
               'selected_week': int(week_number),
               'week_date': week_date,
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