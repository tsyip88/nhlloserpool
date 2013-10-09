import matchups.models
import teams.models
import urllib
import time                                                                                                                                                                                             
from HTMLParser import HTMLParser
import datetime
import re
import string
import pytz

class MatchupDataRetriever:
    @staticmethod    
    def load_matchups():
        #url = "http://www.nhl.com/ice/schedulebyseason.htm"
        url = "/home/tyip/workspace/loserpool/tpt.html"
        contents, success = MatchupDataRetriever.retrieve_site_contents(url)        
        if not success:
            print "failed to load contents from: " + url
            return False
        successfully_processed = MatchupDataRetriever.process_data(contents)
        if successfully_processed:
            print "successfully loaded matchups"
            return True
        print "contents: " + str(contents)                                                                                                      
        return False

    @staticmethod
    def retrieve_site_contents(url):
        file_handle = urllib.urlopen(url)
        contents = file_handle.read()
        # This is necessary because espn has restricted the frequency of API calls to
        # 3 calls per second
        time.sleep(0.4)
        return contents, True

    @staticmethod
    def process_data(contents):
        html_processor = MatchupScheduleParser()
        html_processor.feed(contents)
        return True

DATE_FIELD_WIDTH = 170    
START_YEAR = 2013
MONTH_STRING_TO_INTEGER_HASH = {'Jan':1,
                                'Feb':2,
                                'Mar':3,
                                'Apr':4,
                                'May':5,
                                'Jun':6,
                                'Jul':7,
                                'Aug':8,
                                'Sep':9,
                                'Oct':10,
                                'Nov':11,
                                'Dec':12,}
TEAMS_COLUMN = 1
TIME_COLUMN = 2

class MatchupScheduleParser(HTMLParser):
    in_date_field = False
    in_time_field = False
    date = None
    date_time = None
    home_team = None
    away_team = None
    in_team_name_field = False
    eastern = pytz.timezone('US/Eastern')
    mountain = pytz.timezone('US/Mountain')
    
    def handle_starttag(self, tag, attrs):
        if self.attr_contains_val(attrs, 'class', 'skedStartDateSite'):
            self.in_date_field = True
        if self.attr_contains_val(attrs, 'class', 'skedStartTimeEST'):
            self.in_time_field = True
        if self.attr_contains_val(attrs, 'class', 'teamName'):
            self.in_team_name_field = True
        if self.attr_contains_val(attrs, 'shape', 'rect') and self.in_team_name_field:
            if not self.away_team:
                team_abbrev = self.get_attr_val(attrs, 'rel')
                self.away_team = teams.models.Team.objects.get(abbreviation=team_abbrev)
            else:
                team_abbrev = self.get_attr_val(attrs, 'rel')
                self.home_team = teams.models.Team.objects.get(abbreviation=team_abbrev)
        if tag == 'span':
            self.save_matchup_if_have_valid_data()
            self.date = None
            self.date_time = None
            self.home_team = None
            self.away_team = None
            
    def handle_data(self, data):
        if self.in_date_field:
            self.date = self.parse_date(data)
        if self.in_time_field:
            self.date_time = self.parse_date_time(data)
            
    def handle_endtag(self, tag):
        self.in_date_field = False
        self.in_time_field = False
        if tag == 'div':
            self.in_team_name_field = False
            
    def attr_contains_val(self, attrs, attr_name, attr_value):
        for attr in attrs:
            if attr[0] == attr_name and string.find(attr[1], attr_value) > -1:
                return True
        return False

    def get_attr_val(self, attrs, attr_name):
        for attr in attrs:
            if attr[0] == attr_name:
                return attr[1]
        return None
     
    def save_matchup_if_have_valid_data(self):
        if self.home_team and self.away_team and self.date_time:
            #print "Saving as: %s, %s, %s" %(self.away_team,self.home_team, self.date_time)
            matchup = matchups.models.Matchup(home_team=self.home_team, away_team=self.away_team, date_time=self.date_time)
            matchup.save()
                        
    def parse_date(self, data):
        search_results = re.search(r"\w+ (\w+) (\d+), (\d+)", data)
        if search_results:
            month = MONTH_STRING_TO_INTEGER_HASH.get(search_results.group(1))
            if month == 0:
                return None
            day = int(search_results.group(2))
            year = int(search_results.group(3))
            parsed_date = datetime.date(year, month, day)
            return parsed_date
        else:
            return None      
                    
    def parse_date_time(self, data):
        if not self.date:
            return None
        search_results = re.search(r"(\d+):(\d+) (\w+) (\w+)", data)
        if search_results:
            year = self.date.year
            month = self.date.month
            day = self.date.day
            hour = int(search_results.group(1))
            minute = int(search_results.group(2))
            am_vs_pm = search_results.group(3)
            if am_vs_pm == 'PM':
                hour += 12
            if hour > 23:
                hour -= 12
            parsed_date_time = datetime.datetime(year,
                                                 month,
                                                 day,
                                                 hour,
                                                 minute)
            return self.eastern.localize(parsed_date_time)
        else:
            return None