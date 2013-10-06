from matchups.models import Pick, Matchup
from matchups import utilities
from django import forms

class PickForm(forms.ModelForm):
    class Meta:
        model = Pick
        fields = {'selected_team'}
    def __init__(self, *args, **kwargs):
        super(PickForm, self).__init__(*args, **kwargs)
        widget_choices = [('','')]
        if self.instance:
            week_number = self.instance.week_number 
            previously_selected_teams = Pick.objects.filter(pick_set=self.instance.pick_set).exclude(week_number=week_number).values_list('selected_team', flat=True)
            team_choices = utilities.get_list_of_choices_for_week(week_number)
            for team in team_choices:
                if team.id not in previously_selected_teams:
                    widget_choices.append((team.id, team.full_name()))
        self.fields['selected_team'].widget.choices = widget_choices
        pick_label = "Loser pick " + str(self.instance.pick_set.letter_id())
        self.fields['selected_team'].label = pick_label
        
class MatchupForm(forms.ModelForm):
    class Meta:
        model = Matchup
        fields = {'home_team_score', 'away_team_score', 'went_to_shootout'}