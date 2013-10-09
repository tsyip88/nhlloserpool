from django.db import models
from teams.models import Team
from django.contrib.auth.models import User
from matchups.matchup_defs import CURRENT_TIMEZONE
import pytz

class Matchup(models.Model):
    home_team = models.ForeignKey(Team, related_name="home_team")
    away_team = models.ForeignKey(Team, related_name="away_team")
    home_team_score = models.SmallIntegerField(default=-1)
    away_team_score = models.SmallIntegerField(default=-1)
    went_to_shootout = models.BooleanField(default=False)
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
    def number(self):
        index = 0
        for pick in PickSet.objects.filter(user=self.user):
            index += 1
            if pick.id == self.id:
                return index
        return 0
    
    def __unicode__(self): 
        return self.user.username + " - " + str(self.number())
    
    def is_pick_set_invalid(self):
        pick_values = Pick.objects.filter(pick_set__id=self.id).values_list('is_winning_pick', flat=True)
        return True in pick_values

class Pick(models.Model):
    selected_team = models.ForeignKey(Team)
    week_number = models.SmallIntegerField(default=-1)
    pick_set = models.ForeignKey(PickSet)
    is_winning_pick = models.BooleanField(default=False)
    def __unicode__(self): 
        return str(self.pick_set)+ " - Week " + str(self.week_number)