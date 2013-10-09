from django.shortcuts import render
from django.contrib.auth.decorators import permission_required
from matchups.forms import MatchupForm
from matchups import utilities
from matchups.models import Pick

def update_current_scores(request):
    return update_scores_for_week(request, utilities.current_week_number())

@permission_required('matchups.add_matchup')
def update_scores_for_week(request, week_number):
    weeks = range(1,utilities.current_week_number()+1)
    week_date = str(utilities.game_day(week_number).strftime("%b %d, %Y"))
    forms = list()
    matchup_list = utilities.matchups_for_week(week_number)
    for matchup in matchup_list:
        forms.append(create_form_for_matchup_scores(matchup, request))
    if request.method =="POST":
        picks = Pick.objects.filter(week_number=week_number)
        utilities.update_winning_picks_for_week(week_number, picks)
    context = {'weeks': weeks,
               'selected_week': int(week_number),
               'week_date': week_date,
               'forms': forms}
    return render(request, 'update_scores.html', context)

def create_form_for_matchup_scores(matchup, request):
    if request.method == "POST":
        matchup_form = MatchupForm(request.POST, instance=matchup, prefix=matchup.id)
        if matchup_form.is_valid():
            matchup_form.save()
    else:
        matchup_form = MatchupForm(instance=matchup, prefix=matchup.id)
    return matchup_form