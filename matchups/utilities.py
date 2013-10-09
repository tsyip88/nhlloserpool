import datetime
import pytz
import math
from matchup_defs import FIRST_GAME_DAY, DAYS_IN_A_WEEK, CURRENT_TIMEZONE, UTC_TIMEZONE
from teams.models import Team
from matchups.models import PickSet, Pick, Matchup
from django.contrib.auth.models import User
from django.db.models import Q

def game_day(week_number):
    offset_from_week_1 = datetime.timedelta(weeks = int(week_number)-1)
    game_day = FIRST_GAME_DAY + offset_from_week_1
    return game_day

def week_is_over(week_number):
    game_day = FIRST_GAME_DAY
    day_after_game_day = game_day + datetime.timedelta(days=1);
    matchups = Matchup.objects.filter(date_time__gte=game_day,date_time__lt=day_after_game_day, home_team_score=-1, away_team_score=-1)
    return matchups.count()==0

def current_week_number():
    time_elapsed_since_week_1 = datetime.datetime.now(pytz.timezone(CURRENT_TIMEZONE))-FIRST_GAME_DAY
    if(time_elapsed_since_week_1.total_seconds() < 0):
        return 1
    else:
        return (int(time_elapsed_since_week_1.days)/DAYS_IN_A_WEEK) + 1
    
def current_submit_picks_week_number():
    current_week = current_week_number()
    if week_is_over(current_week):
        return current_week+1
    return current_week

def week_number_for_matchup(matchup):
    matchup_date = matchup.date_time
    offset_from_week_1 = matchup_date - FIRST_GAME_DAY
    week_number = math.floor((offset_from_week_1.days/DAYS_IN_A_WEEK))+1
    return int(week_number)
    
def matchups_for_week(week_number):
    game_day = FIRST_GAME_DAY
    day_after_game_day = game_day + datetime.timedelta(days=1);
    matchups = Matchup.objects.filter(date_time__gte=game_day, date_time__lt=day_after_game_day)
    return matchups
    
def users_that_have_submitted_picks_for_week(week_number):
    user_list = list()
    for user in User.objects.all():
        if Pick.objects.filter(user=user, week_number=week_number).count() > 0:
            user_list.append(user)
    return user_list
    
def pick_sets_for_user(user):
    return PickSet.objects.filter(user=user)

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
        if matchup.went_to_shootout:
            winning_teams.append(matchup.home_team)
            winning_teams.append(matchup.away_team)
        else:
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