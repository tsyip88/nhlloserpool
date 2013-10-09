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
            team_choices = utilities.get_list_of_choices_for_week(week_number)
            for team in team_choices:
                widget_choices.append((team.id, team.full_name()))
        self.fields['selected_team'].widget.choices = widget_choices
        pick_label = "Loser pick " + str(self.instance.pick_set.number())
        self.fields['selected_team'].label = pick_label
        
class MatchupForm(forms.ModelForm):
    class Meta:
        model = Matchup
        fields = {'home_team_score', 'away_team_score', 'went_to_shootout'}