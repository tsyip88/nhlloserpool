import teams.models
import urllib
import json
import time
import re
import string
from HTMLParser import HTMLParser


class TeamDataRetriever:
    @staticmethod    
    def load_teams(sport_name, league_name):
        espnUrl = "http://api.espn.com/v1/sports/" + sport_name + "/" + league_name + "?apikey=qvf4w5he6tszff4j3y3ugvus"
        contents, success = TeamDataRetriever.retrieve_json_contents(espnUrl)        
        if success:
            successfully_extracted = TeamDataRetriever.extract_league_data(contents, sport_name, league_name)
            if successfully_extracted:
                print "successfully loaded league"
                return True
        print "failed to load teams, read from: " + espnUrl
        print "contents: " + str(contents)
        return False  

    @staticmethod
    def retrieve_json_contents(url):
        success = False
        file_handle = urllib.urlopen(url)
        json_data = file_handle.read()
        contents = json.loads(json_data)
        if contents['status'] == "success":
            success = True
        # This is necessary because espn has restricted the frequency of API calls to
        # 3 calls per second
        time.sleep(0.4)
        return contents, success

    @staticmethod
    def extract_league_data(contents, sport_name, league_name):
        print "-----------"
        extracted_league = contents['sports'][0]['leagues'][0]
        extracted_conferences = extracted_league['groups']
        
        new_league = teams.models.League()
        new_league.abbreviation = extracted_league['abbreviation'].upper()
        new_league.name = extracted_league['name']
        new_league.save()
        for extracted_conference in extracted_conferences:
            new_conference = teams.models.Conference()
            new_conference.abbreviation = extracted_conference['abbreviation'].upper()
            new_conference.name = extracted_conference['name']
            new_conference.league = new_league
            new_conference.save()
            
            if new_conference.name == 'Western Conference':
                new_division = teams.models.Division()
                new_division.abbreviation = 'CEN'
                new_division.name = 'Central Division'
                new_division.conference = new_conference
                new_division.save()
                new_division2 = teams.models.Division()
                new_division2.abbreviation = 'PAC'
                new_division2.name = 'Pacific Division'
                new_division2.conference = new_conference
                new_division2.save()
            if new_conference.name == 'Eastern Conference':
                new_division = teams.models.Division()
                new_division.abbreviation = 'ATL'
                new_division.name = 'Atlantic Division'
                new_division.conference = new_conference
                new_division.save()
                new_division2 = teams.models.Division()
                new_division2.abbreviation = 'MET'
                new_division2.name = 'Metropolitan Division'
                new_division2.conference = new_conference
                new_division2.save()

        espnUrl = "http://api.espn.com/v1/sports/" + sport_name + "/" + league_name + "/teams?apikey=qvf4w5he6tszff4j3y3ugvus"                
        contents, success = TeamDataRetriever.retrieve_json_contents(espnUrl)
                
        if success:
            extracted_teams = contents['sports'][0]['leagues'][0]['teams']
            for extracted_team in extracted_teams:
                new_team = teams.models.Team()
                new_team.abbreviation = extracted_team['abbreviation'].upper()
                new_team.name = extracted_team['name']
                new_team.location = extracted_team['location']
                new_team.division = teams.models.Division.objects.get(id=1)
                new_team.save()
                print "saving: " + new_team.name
            else:
                print "failed to load divisions, read from: " + espnUrl
                print "contents: " + str(contents)
                return False
        print "-----------"
        return True
    
    @staticmethod    
    def load_teams2(sport_name, league_name):
        url = "http://espn.go.com/"+ league_name+ "/teams"
        contents, success = TeamDataRetriever.retrieve_site_contents(url)        
        if not success:
            print "failed to load contents from: " + url
            return False
        successfully_processed = TeamDataRetriever.process_data(contents)
        if successfully_processed:
            print "successfully loaded matchups"
            return True
        print "contents: " + str(contents)                                                                                                      
        return False
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
        html_processor = TeamListParser()
        html_processor.feed(contents)
        return True
    
class TeamListParser(HTMLParser):
    in_h1 = False
    in_colhead = False
    in_date_field = False
    matchups = list()
    last_retrieved_date = None
    in_matchup_row = False
    col_num = 0
    need_away_team = True
    home_team = None
    away_team = None
    date_time = None
    
    def handle_starttag(self, tag, attrs):
        if tag == 'h4':
            if self.attr_contains_val(attrs,'class','colhead'):
                self.in_h1 = True
            
    def handle_data(self, data):
        if self.in_h1:
            search_results = re.search(r"(.+) Division", data)
            if search_results:
                division_name = search_results.group(1)
                print division_name
            
    def handle_endtag(self, tag):
        if tag=='tr':
            if self.in_matchup_row:
                self.save_matchup_if_have_valid_data()
            self.in_colhead = False
            self.in_matchup_row = False
            self.col_num = 0
        if tag == 'td':
            self.in_date_field = False
            
    def attr_contains_val(self, attrs, attr_name, attr_value):
        for attr in attrs:
            if attr[0] == attr_name and string.find(attr[1], attr_value) > -1:
                return True
        return False