from django.db import models
from teams.models import Team
from django.contrib.auth.models import User
from matchups.matchup_defs import CURRENT_TIMEZONE
import utilities
import pytz

class Matchup(models.Model):
    home_team = models.ForeignKey(Team, related_name="home_team")
    away_team = models.ForeignKey(Team, related_name="away_team")
    home_team_score = models.SmallIntegerField(default=-1)
    away_team_score = models.SmallIntegerField(default=-1)
    date_time = models.DateTimeField()
    
    def date_time_string(self):
        fmt = "%A, %b %d - %I:%M %p"
        return self.date_time.astimezone(pytz.timezone(CURRENT_TIMEZONE)).strftime(fmt)
    
    def full_name(self):
        return self.date_time_string() + ' - ' + self.away_team.full_name() + ' at ' + self.home_team.full_name()
    
    def __unicode__(self): 
        return self.full_name()
    
    def winning_team(self):
        if self.home_team_score < 0 or self.away_team_score < 0:
            return None
        if self.home_team_score > self.away_team_score:
            return self.home_team
        else:
            return self.away_team
    
class PickSet(models.Model):
    user = models.ForeignKey(User)
    def letter_id(self):
        index = 0
        for pick in PickSet.objects.filter(user=self.user):
            if pick.id == self.id:
                return chr(ord('A')+index)
            index += 1
        return 0
    
    def __unicode__(self): 
        return self.user.username + " - " + str(self.letter_id())
    
    def is_eliminated(self):
        pick_values = Pick.objects.filter(pick_set__id=self.id).values_list('is_winning_pick', flat=True)
        picked_wrong = True in pick_values 
        minimum_number_of_picks = int(utilities.current_week_number())-1
        missed_a_week = Pick.objects.filter(pick_set__id=self.id).count() < minimum_number_of_picks
        return picked_wrong or missed_a_week

class Pick(models.Model):
    selected_team = models.ForeignKey(Team)
    week_number = models.SmallIntegerField(default=-1)
    pick_set = models.ForeignKey(PickSet)
    is_winning_pick = models.BooleanField(default=False)
    def __unicode__(self): 
        return str(self.pick_set)+ " - Week " + str(self.week_number)