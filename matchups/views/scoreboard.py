from django.shortcuts import render
from django.contrib.auth.decorators import permission_required
from matchups import utilities, model_utilities
from matchups.models import PickSet
    
@permission_required('matchups.add_matchup')
def admin_scoreboard_for_week(request, week_number):
    return scoreboard(request, week_number, True)

def scoreboard_current_week(request):
    return scoreboard(request, utilities.current_week_number())
    
def scoreboard(request, week_number, is_admin=False):
    pick_sets = PickSet.objects.prefetch_related('pick_set')
    week_has_started = model_utilities.has_first_matchup_of_week_started(week_number)
    current_week = int(utilities.current_week_number())
    
    row_sets = dict()
    for pick_set in pick_sets:
        pick_user = pick_set.user
        row_set = get_or_create_row_set(row_sets, pick_user, request.user)
        row_set.rowspan += 1
        picks = pick_set.pick_set.all()
        table_row = PickRow()
        table_row.letter_id = pick_set.letter_id
        table_row.pick_row_items = list()
        pick_set_is_eliminated = False
        number_of_picks = 0
        for pick in picks:
            number_of_picks += 1
            row_item = PickRowItem()
            row_item.show_pick = is_admin or row_set.is_current_user or week_has_started or pick.week_number != current_week
            row_item.is_winning_pick = pick.is_winning_pick
            pick_set_is_eliminated |= row_item.is_winning_pick 
            row_item.team_image_location = pick.selected_team.image_location
            row_item.team_name = pick.selected_team.full_name()
            table_row.pick_row_items.append(row_item)
        minimum_number_of_picks = int(utilities.current_week_number())-1
        missed_a_week = number_of_picks < minimum_number_of_picks
        pick_set_is_eliminated |= missed_a_week
        table_row.pick_set_is_eliminated = pick_set_is_eliminated
        row_set.user_is_eliminated &= pick_set_is_eliminated
        for i in range(0, current_week-len(table_row.pick_row_items)):
            row_item = PickRowItem()
            row_item.is_unavailable = table_row.pick_set_is_eliminated
            table_row.pick_row_items.append(row_item)
        row_set.pick_rows.append(table_row)
    ordered_row_sets = list()
    eliminated_row_sets = list()
    for row_set in row_sets.values():
        if row_set.user_is_eliminated:
            eliminated_row_sets.append(row_set)
        elif row_set.is_current_user:
            ordered_row_sets.insert(0, row_set)
        else:
            ordered_row_sets.append(row_set)
    ordered_row_sets.extend(eliminated_row_sets)
    week_date = str(utilities.game_day(week_number).strftime("%b %d, %Y"))
    context = {'current_week': current_week,
               'selected_week': int(week_number),
               'week_date': week_date,
               'row_sets':ordered_row_sets}
    return render(request, 'scoreboard.html', context)

def get_or_create_row_set(row_sets, user, current_user):
    if not row_sets.has_key(user):
        row_sets[user] = RowSet()
        row_sets[user].user_name = user_display_name(user)
        row_sets[user].pick_rows = list()
        row_sets[user].is_current_user = current_user == user
    return row_sets[user]

def user_display_name(user):
    if user.first_name:
        return user.first_name
    return user.username

class RowSet:
    rowspan = 0
    user_is_eliminated = True
    user_name = None
    pick_rows = list()
    is_current_user = False

class PickRow:
    pick_set_is_eliminated = False
    letter_id = 'A'
    pick_row_items = list()
    
class PickRowItem:
    show_pick = False
    is_winning_pick = False
    team_image_location = ''
    team_name = ''
    is_unavailable = False
    