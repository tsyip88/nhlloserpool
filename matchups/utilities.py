import datetime
import pytz
import math
from matchup_defs import FIRST_GAME_DAY, DAYS_IN_A_WEEK, CURRENT_TIMEZONE

def game_day(week_number):
    offset_from_week_1 = datetime.timedelta(weeks = int(week_number)-1)
    game_day = FIRST_GAME_DAY + offset_from_week_1
    return game_day

def current_week_number():
    time_elapsed_since_week_1 = datetime.datetime.now(pytz.timezone(CURRENT_TIMEZONE))-FIRST_GAME_DAY
    if(time_elapsed_since_week_1.days <= 0):
        return 1
    else:
        return ((int(time_elapsed_since_week_1.days)-1)/DAYS_IN_A_WEEK) + 2

def week_number_for_matchup(matchup):
    matchup_date = matchup.date_time
    offset_from_week_1 = matchup_date - FIRST_GAME_DAY
    week_number = math.floor((offset_from_week_1.days/DAYS_IN_A_WEEK))+1
    return int(week_number)