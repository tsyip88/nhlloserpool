from django.db import models

class League(models.Model):
    name = models.CharField(max_length=50)
    abbreviation = models.CharField(max_length=5)
    
    def __unicode__(self):
        return self.name
    
class Conference(models.Model):
    league = models.ForeignKey(League)
    name = models.CharField(max_length=50)
    abbreviation = models.CharField(max_length=5)
    
    def __unicode__(self):
        return self.name

class Division(models.Model):
    conference = models.ForeignKey(Conference)
    name = models.CharField(max_length=50)
    abbreviation = models.CharField(max_length=5)
    
    def __unicode__(self):
        return self.name

class Team(models.Model):
    division = models.ForeignKey(Division)
    location = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    abbreviation = models.CharField(max_length=5)
    image_location = models.CharField(max_length=50)
    
    def full_name(self):
        return self.location + ' ' + self.name
    
    def __unicode__(self):
        return self.full_name()
    
    def schedule_lookup_name(self):
        if self.full_name() == 'New York Giants':
            return 'NY Giants'
        if self.full_name() == 'New York Jets':
            return 'NY Jets'
        return self.location