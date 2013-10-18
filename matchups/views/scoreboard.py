from django.shortcuts import render
from django.contrib.auth.decorators import permission_required
from matchups import utilities, model_utilities
from matchups.models import PickSet, Pick
import datetime
    
@permission_required('matchups.add_matchup')
def admin_scoreboard_for_week(request, week_number):
    return scoreboard(request, week_number, True)

def scoreboard_current_week(request):
    return scoreboard(request, utilities.current_week_number())
    
def scoreboard(request, week_number, is_admin=False):
    ct1 = datetime.datetime.now()
    print ct1
    pick_sets = order_list(request.user)
    table_rows = list()
    week_has_started = model_utilities.has_first_matchup_of_week_started(week_number)
    current_week = int(utilities.current_week_number())
    #PickSet.objects.select_related()
    #Pick.objects.prefetch_related('pick_set')
    
    row_sets = dict()
    for pick_set in pick_sets:
#     for pick_set_id in pick_set_ids:
#         pick_set = PickSet.objects.select_related('user').get(id=pick_set_id)
        ct = datetime.datetime.now()
        print ct
        pick_user = pick_set.user
        row_set = get_or_create_row_set(row_sets, pick_user)
        row_set.rowspan += 1
        pick_set_is_eliminated = pick_is_eliminated(pick_set)
        if pick_set_is_eliminated:
            row_set.user_is_eliminated = True
        
        table_row = PickRow()
        table_row.pick_set_is_eliminated = pick_set_is_eliminated
        table_row.letter_id = pick_set.letter_id()
        
        table_row.pick_row_items = list()
#         pick_ids = Pick.objects.filter(pick_set=pick_set).order_by('week_number').values_list('id', flat=True)
#         for pick_id in pick_ids:
#             pick = Pick.objects.get(id=pick_id)

        picks = Pick.objects.filter(pick_set=pick_set).order_by('week_number')
        for pick in picks:
            row_item = PickRowItem()
            is_current_user = pick_set.user == request.user
            row_item.show_pick = is_admin or is_current_user or week_has_started or pick.week_number != current_week
            row_item.is_winning_pick = pick.is_winning_pick
            row_item.team_image_location = pick.selected_team.image_location
            row_item.team_name = pick.selected_team.full_name()
            table_row.pick_row_items.append(row_item)
        for i in range(0, current_week-len(table_row.pick_row_items)):
            row_item = PickRowItem()
            row_item.is_unavailable = table_row.pick_set_is_eliminated
            table_row.pick_row_items.append(row_item)
        row_set.pick_rows.append(table_row)
    week_date = str(utilities.game_day(week_number).strftime("%b %d, %Y"))
    context = {'current_week': current_week,
               'selected_week': int(week_number),
               'week_date': week_date,
               'row_sets':row_sets.values()}
    ct2 = datetime.datetime.now()
    print ct2
    print ct2-ct1
    return render(request, 'scoreboard.html', context)

def get_or_create_row_set(row_sets, user):
    if not row_sets.has_key(user):
        row_sets[user] = RowSet()
        row_sets[user].user_name = user_display_name(user)
        row_sets[user].pick_rows = list()
    return row_sets[user]

def pick_is_eliminated(pick_set):
    pick_values = Pick.objects.filter(pick_set__id=pick_set.id).values_list('is_winning_pick', flat=True)
    picked_wrong = True in pick_values 
    minimum_number_of_picks = int(utilities.current_week_number())-1
    missed_a_week = Pick.objects.filter(pick_set__id=pick_set.id).count() < minimum_number_of_picks
    return picked_wrong or missed_a_week
    
def user_is_eliminated(user):   
    sets_for_user = PickSet.objects.filter(user=user)
    for pick_set in sets_for_user:
        if not pick_is_eliminated(pick_set):
            return False
    return True

def user_display_name(user):
    if user.first_name:
        return user.first_name
    return user.username
    
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

class RowSet:
    rowspan = 0
    user_is_eliminated = False
    user_name = None
    pick_rows = list()

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
    