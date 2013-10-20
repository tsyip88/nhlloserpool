from matchup_defs import FIRST_GAME_DAY, DAYS_IN_A_WEEK, UTC_TIMEZONE
from matchups.models import PickSet, Matchup, Pick
from teams.models import Team
from django.contrib.auth.models import User
from django.db.models import Q
import datetime
import pytz
    
def pick_sets_for_user(user):
    return PickSet.objects.filter(user=user)

def week_is_over(week_number):
    game_day = FIRST_GAME_DAY
    day_after_game_day = game_day + datetime.timedelta(days=1);
    matchups = Matchup.objects.filter(date_time__gte=game_day,date_time__lt=day_after_game_day, home_team_score=-1, away_team_score=-1)
    return matchups.count()==0
    
def matchups_for_week(week_number):
    days_from_first_game = DAYS_IN_A_WEEK*(int(week_number)-1)
    game_day = FIRST_GAME_DAY +  datetime.timedelta(days=days_from_first_game)
    day_after_game_day = game_day + datetime.timedelta(days=1);
    matchups = Matchup.objects.filter(date_time__gte=game_day, date_time__lt=day_after_game_day)
    return matchups
    
def users_that_have_submitted_picks_for_week(week_number):
    user_list = list()
    for user in User.objects.all():
        if Pick.objects.filter(user=user, week_number=week_number).count() > 0:
            user_list.append(user)
    return user_list

def get_or_create_pick(week_number, pick_set):
    picks_for_matchup = Pick.objects.filter(pick_set=pick_set, week_number=week_number)
    if picks_for_matchup.count() > 0:
        pick = picks_for_matchup[0]
    else:
        pick = Pick(week_number=week_number, pick_set=pick_set)
    return pick

def datetime_for_first_matchup(week_number):
    matchups = matchups_for_week(week_number).order_by('date_time')
    if matchups.count() > 0:
        return matchups[0].date_time
    return None

def has_first_matchup_of_week_started(week_number):
    return datetime.datetime.now(pytz.timezone(UTC_TIMEZONE)) > datetime_for_first_matchup(week_number)

def get_list_of_choices_for_week(week_number):
    home_team_ids = matchups_for_week(week_number).values_list('home_team_id', flat=True)
    away_team_ids = matchups_for_week(week_number).values_list('away_team_id', flat=True)
    choices = Team.objects.filter(Q(id__in=home_team_ids) | Q(id__in=away_team_ids)).order_by('location','name')
    return choices

def winning_teams_for_week(week_number):
    matchups = matchups_for_week(week_number)
    winning_teams = list()
    for matchup in matchups:
        winning_team = matchup.winning_team()
        if winning_team:
            winning_teams.append(winning_team)
    return winning_teams
        
def update_winning_picks_for_week(week_number, picks):
    winning_teams = winning_teams_for_week(week_number)
    for pick in picks:
        print pick.selected_team
        if pick.selected_team in winning_teams:
            pick.is_winning_pick = True
        else:
            pick.is_winning_pick = False
        pick.save(update_fields=['is_winning_pick'])